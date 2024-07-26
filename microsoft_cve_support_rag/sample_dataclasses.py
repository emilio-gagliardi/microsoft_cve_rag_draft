from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class JobPosting(BaseModel):
    database_id: str = Field(
        ..., description="UUID string for the database containing job postings"
    )
    posting_id: str = Field(..., description="UUID string for a specific job posting")
    posting_url: str = Field(..., description="URL of the job posting")
    company_base_url: str = Field(..., description="Base URL of the company's website")
    company_name: str = Field(..., description="Name of the company")
    posting_text: str = Field(..., description="Full text content of the job posting")


class ScrapedPage(BaseModel):
    url: str = Field(default="", description="The URL of the scraped page")
    content: str = Field(default="", description="The content of the scraped page")


class CompanyResearchTask(BaseModel):
    query: str = Field(
        default="", description="The search query string generated for this task"
    )
    results: list[dict] = Field(
        default_factory=list, description="The full search results"
    )
    urls: list[str] = Field(
        default_factory=list,
        description="List of URLs extracted from the search results",
    )


class DomainAnalysis(BaseModel):
    base_url: Optional[str] = Field(
        default="", description="The base URL of the website"
    )
    sitemap_found: Optional[bool] = Field(
        default=None, description="Whether a sitemap was found"
    )
    scraped_pages: List[ScrapedPage] = Field(
        default_factory=list, description="List of scraped pages"
    )


class CompanyResearch(BaseModel):
    company_name: str = Field(
        default="", description="Name of the company being researched"
    )
    domain_analysis: DomainAnalysis = Field(
        ..., description="Results from the company domain analysis"
    )
    technical_research: CompanyResearchTask = Field(
        ..., description="Results from the technical research task"
    )
    business_research: CompanyResearchTask = Field(
        ..., description="Results from the business/operations research task"
    )


class TextObject(BaseModel):
    type: str = "text"
    text: Dict[str, Any]


class RichText(BaseModel):
    rich_text: List[TextObject]


class Paragraph(BaseModel):
    rich_text: List[TextObject]


class Heading(BaseModel):
    rich_text: List[TextObject]


class Heading1(BaseModel):
    rich_text: List[TextObject]


class Heading2(BaseModel):
    rich_text: List[TextObject]


class Heading3(BaseModel):
    rich_text: List[TextObject]


class ListItem(BaseModel):
    rich_text: List[TextObject]


class BulletedListItem(BaseModel):
    rich_text: List[TextObject]


class NumberedListItem(BaseModel):
    rich_text: List[TextObject]


class Quote(BaseModel):
    rich_text: List[TextObject]


class Block(BaseModel):
    object: str = "block"
    type: str
    paragraph: Optional[Paragraph] = None
    heading_1: Optional[Heading1] = None
    heading_2: Optional[Heading2] = None
    heading_3: Optional[Heading3] = None
    bulleted_list_item: Optional[BulletedListItem] = None
    numbered_list_item: Optional[NumberedListItem] = None
    quote: Optional[Quote] = None


class Parent(BaseModel):
    type: str
    page_id: str


class Icon(BaseModel):
    emoji: str


class External(BaseModel):
    url: Optional[str]


class Cover(BaseModel):
    type: str
    external: External


class Annotations(BaseModel):
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: str = "default"


class Text(BaseModel):
    content: str
    link: Optional[str] = None


class TitleContent(BaseModel):
    type: str
    text: Text
    annotations: Annotations
    plain_text: str
    href: Optional[str] = None


class Property(BaseModel):
    id: str
    type: str
    title: List[TitleContent]


class Properties(BaseModel):
    Title: Property


class NotionPage(BaseModel):
    parent: Parent
    icon: Optional[Icon] = None
    cover: Optional[Cover] = None
    properties: Properties
    children: List[Block]


class NotionPageEntity(BaseModel):
    page_id: str
    parent_id: str
    title: str
    created_time: Optional[str] = None
    last_edited_time: Optional[str] = None
    url: Optional[str] = None


class NotionPageEntityList(BaseModel):
    pages: List[NotionPageEntity]
