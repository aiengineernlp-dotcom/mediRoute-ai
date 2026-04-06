# llm_client_retry.py
"""
Production LLM Client with Retry Logic.
Use case: Resilient LLM API calls with exponential backoff.
Pattern: Used in ALL production AI systems.
Stack: Exceptions + Context managers → foundation for LangChain clients.
"""
import time
import random
from contextlib import contextmanager


# Exceptions personnalisées
class LLMError(Exception):
    """Base LLM error."""
    pass

class RateLimitError(LLMError):
    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(f"Rate limit. Retry after {retry_after}s")

class APITimeoutError(LLMError):
    def __init__(self, timeout: int):
        super().__init__(f"API timeout after {timeout}s")

class InvalidRequestError(LLMError):
    """Non-recoverable — bad prompt or params."""
    pass

class ModelNotAvailableError(LLMError):
    """Model is down or deprecated."""
    pass


@contextmanager
def llm_call_timer(model: str):
    """Context manager to time and log LLM calls."""
    start = time.time()
    print(f"  ▶ Calling {model}...")
    try:
        yield
        elapsed = time.time() - start
        print(f"  ✅ Success in {elapsed:.3f}s")
    except Exception as e:
        elapsed = time.time() - start
        print(f"  ❌ Failed after {elapsed:.3f}s: {type(e).__name__}")
        raise


def mock_api_call(prompt: str, model: str,
                  fail_rate: float = 0.4) -> dict:
    """
    Simulate an LLM API call with random failures.
    fail_rate: probability of failure on each attempt.
    """
    time.sleep(0.05)  # simulate network latency

    rand = random.random()

    if rand < fail_rate * 0.3:
        raise RateLimitError(retry_after=2)
    elif rand < fail_rate * 0.6:
        raise APITimeoutError(timeout=30)
    elif rand < fail_rate:
        raise LLMError("Internal server error")

    # Succès
    return {
        "model":   model,
        "content": f"[Mock response to: {prompt[:40]}...]",
        "usage":   {
            "prompt_tokens":     len(prompt.split()),
            "completion_tokens": 50,
            "total_tokens":      len(prompt.split()) + 50
        }
    }


def call_with_retry(
    prompt: str,
    model: str = "gpt-4o",
    max_retries: int = 3,
    base_delay: float = 1.0,
    fallback_model: str = "gpt-4o-mini"
) -> dict:
    """
    Call LLM API with exponential backoff retry.

    Strategy:
        - RateLimitError → wait then retry
        - APITimeoutError → retry immediately (up to max)
        - InvalidRequestError → fail fast (no retry)
        - All retries exhausted → try fallback model
    """
    last_error = None

    for attempt in range(1, max_retries + 1):
        current_model = model if attempt <= max_retries else fallback_model

        try:
            with llm_call_timer(current_model):
                result = mock_api_call(prompt, current_model)
            return {**result, "attempts": attempt, "final_model": current_model}

        except InvalidRequestError as e:
            # Non-récupérable — arrêt immédiat
            raise RuntimeError(
                f"Invalid request (no retry): {e}"
            ) from e

        except RateLimitError as e:
            wait = min(base_delay * (2 ** attempt), 30)
            print(f"  ⏳ Rate limited. Waiting {wait:.1f}s "
                  f"(attempt {attempt}/{max_retries})")
            time.sleep(wait)
            last_error = e

        except (APITimeoutError, LLMError) as e:
            if attempt < max_retries:
                wait = base_delay * attempt
                print(f"  🔄 Retrying in {wait:.1f}s "
                      f"(attempt {attempt}/{max_retries})")
                time.sleep(wait)
            last_error = e

    # Fallback model
    print(f"\n  ⚠️  Switching to fallback: {fallback_model}")
    try:
        with llm_call_timer(fallback_model):
            result = mock_api_call(prompt, fallback_model, fail_rate=0.1)
        return {**result, "attempts": max_retries + 1,
                "final_model": fallback_model, "used_fallback": True}
    except Exception as e:
        raise RuntimeError(
            f"All retries and fallback failed. Last error: {last_error}"
        ) from e


def display_result(result: dict) -> None:
    print(f"\n{'=' * 50}")
    print(f"{'LLM CALL RESULT':^50}")
    print("=" * 50)
    print(f"  Model         : {result.get('final_model', 'unknown')}")
    print(f"  Attempts      : {result.get('attempts', '?')}")
    print(f"  Fallback used : {result.get('used_fallback', False)}")
    print(f"  Total tokens  : {result['usage']['total_tokens']}")
    print(f"  Content       : {result['content']}")
    print("=" * 50)


# Test
random.seed(42)
prompts = [
    "What is retrieval augmented generation?",
    "Explain vector databases in simple terms",
    "How does LangChain work?",
]

for prompt in prompts:
    print(f"\n{'─' * 50}")
    print(f"Prompt: {prompt}")
    try:
        result = call_with_retry(prompt, max_retries=3)
        display_result(result)
    except RuntimeError as e:
        print(f"  ❌ FATAL: {e}")