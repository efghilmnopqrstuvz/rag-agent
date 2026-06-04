# Document Loaders

Document loaders are the components responsible for bringing external data into a LangChain application. A retrieval system is only as good as the data behind it, and that data lives in many different formats and locations: web pages, PDFs, text files, spreadsheets, databases, and software-as-a-service platforms. The job of a loader is to read from one of these sources and produce a standard internal representation that the rest of the pipeline can work with.

## The Document Object

Every loader returns a list of `Document` objects. A `Document` has two main attributes. The first is `page_content`, which holds the actual text extracted from the source. The second is `metadata`, a dictionary of additional information such as the source URL or file path, a page number, a title, or a timestamp. Metadata is important because it lets you trace an answer back to its origin and because it can later be used to filter retrieval — for example, restricting a search to documents from a particular source.

## Common Loaders

LangChain ships with many loaders. A few that appear frequently:

- **WebBaseLoader** fetches one or more web pages and extracts their text. Under the hood it uses an HTML parser to strip away markup. Because raw web pages contain navigation menus, footers, and other boilerplate, this loader can be configured to keep only the relevant part of the page.
- **PyPDFLoader** reads a PDF file and extracts its text page by page, producing one `Document` per page with the page number stored in metadata.
- **DirectoryLoader** loads every file in a folder that matches a given pattern, delegating each file to an appropriate loader. This is convenient when a knowledge base is provided as a set of local files.
- **TextLoader** reads a plain text file directly.
- **CSVLoader** reads tabular data, typically producing one `Document` per row.

## The Challenge of Clean Extraction

Loading is rarely just a mechanical step. The quality of the extracted text has a direct effect on retrieval quality downstream. Web pages are the hardest case: the same content may be duplicated across linked pages, and navigation elements can leak into the extracted text as noise. When this noise is vectorized, it pollutes the vector store and can cause the retriever to return chunks that contain mostly boilerplate instead of substantive content.

For this reason, in many real projects the cleanest approach is to start from curated documents — files that have already been reviewed and stripped of irrelevant material — rather than scraping live web pages. In an enterprise setting the knowledge base is usually supplied by the client as a set of documents, which sidesteps the extraction-quality problem entirely and lets the team focus on the retrieval and generation stages.

## Loaders in the Pipeline

The loader is the first stage of the ingestion pipeline. Its output — a list of `Document` objects — is passed directly to a text splitter, which breaks the documents into smaller chunks before they are embedded and stored. Because the loader defines what text enters the system, decisions made here ripple through every later stage, which is why choosing the right source and ensuring clean extraction is one of the highest-leverage steps in building a reliable RAG system.
