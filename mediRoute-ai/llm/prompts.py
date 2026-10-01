# prompt_template_engine.py
"""
Prompt Template Engine.
Use case: Manage and version prompt templates for LLM pipelines.
This is exactly what LangChain's PromptTemplate does internally.
Stack: Dicts + Sets + String formatting → foundation for LangChain.
"""


class PromptTemplate:
    """
    Manages prompt templates with variable injection.
    Mirrors LangChain's PromptTemplate class.
    """

    def __init__(self, template: str, version: str = "1.0"):
        self.template = template
        self.version  = version
        # Détecter les variables dans le template
        self.variables: set[str] = self._extract_variables()

    def _extract_variables(self) -> set[str]:
        """Extract variable names from template {var} syntax."""
        import re
        return set(re.findall(r'\{(\w+)\}', self.template))

    def format(self, **kwargs) -> str:
        """
        Inject variables into template.

        Raises:
            ValueError: if required variables are missing
        """
        provided = set(kwargs.keys())
        missing  = self.variables - provided
        extra    = provided - self.variables

        if missing:
            raise ValueError(
                f"Missing variables: {missing}. "
                f"Required: {self.variables}"
            )

        if extra:
            print(f"  ⚠️  Unused variables: {extra}")

        return self.template.format(**kwargs)

    def __repr__(self) -> str:
        return (f"PromptTemplate(version={self.version}, "
                f"vars={self.variables})")


class PromptLibrary:
    """
    Centralized library of prompt templates.
    Use case: Version and manage prompts as code (PromptOps).
    """

    def __init__(self):
        self._templates: dict[str, PromptTemplate] = {}
        self._usage_count: dict[str, int] = {}

    def register(self, name: str,
                 template: PromptTemplate) -> None:
        """Register a template in the library."""
        self._templates[name] = template
        self._usage_count[name] = 0
        print(f"  ✅ Registered: '{name}' "
              f"(vars: {template.variables})")

    def get(self, name: str) -> PromptTemplate:
        """Retrieve a template by name."""
        if name not in self._templates:
            available = list(self._templates.keys())
            raise KeyError(
                f"Template '{name}' not found. "
                f"Available: {available}"
            )
        self._usage_count[name] += 1
        return self._templates[name]

    def render(self, name: str, **kwargs) -> str:
        """Retrieve and render a template in one call."""
        return self.get(name).format(**kwargs)

    def get_most_used(self, top_n: int = 3) -> list[tuple]:
        """Return most used templates."""
        return sorted(
            self._usage_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

    def display_library(self) -> None:
        print("\n" + "=" * 55)
        print(f"{'PROMPT LIBRARY':^55}")
        print("=" * 55)
        for name, tmpl in self._templates.items():
            count = self._usage_count[name]
            print(f"\n  [{name}] v{tmpl.version} | Used: {count}x")
            print(f"  Variables: {tmpl.variables}")
            preview = tmpl.template[:80].replace("\n", " ")
            print(f"  Preview  : {preview}...")
        print("=" * 55)


# Construction de la librairie de prompts
library = PromptLibrary()

print("Registering prompt templates...\n")

library.register("rag_qa", PromptTemplate(
    template="""You are a helpful assistant. Use the following context 
to answer the question. If you don't know, say so.

Context:
{context}

Question: {question}

Answer:""",
    version="2.1"
))

library.register("summarize", PromptTemplate(
    template="""Summarize the following {content_type} in {max_sentences} 
sentences, focusing on {focus_area}:

{content}

Summary:""",
    version="1.3"
))

library.register("classify", PromptTemplate(
    template="""Classify the following text into one of these categories: 
{categories}.

Text: {text}

Respond with only the category name.
Category:""",
    version="1.0"
))

library.register("extract", PromptTemplate(
    template="""Extract {entity_type} from the following text.
Return as a JSON list.

Text: {text}

{entity_type}:""",
    version="1.1"
))

# Test de rendu
print("\n--- RAG QA Prompt ---")
rag_prompt = library.render(
    "rag_qa",
    context="LangChain is a framework for building LLM applications.",
    question="What is LangChain used for?"
)
print(rag_prompt)

print("\n--- Summarize Prompt ---")
summary_prompt = library.render(
    "summarize",
    content_type="technical article",
    max_sentences="3",
    focus_area="key takeaways",
    content="Transformers have revolutionized NLP..."
)
print(summary_prompt)

library.display_library()
print(f"\n  Most used: {library.get_most_used()}")