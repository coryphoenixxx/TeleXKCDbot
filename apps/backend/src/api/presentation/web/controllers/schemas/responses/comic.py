import datetime as dt
from collections.abc import Mapping

from pydantic import BaseModel, HttpUrl

from api.application.dtos.responses import TranslationResponseDTO
from api.application.dtos.responses.comic import ComicResponseDTO, ComicResponseWTranslationsDTO
from api.infrastructure.database.types import Limit, Offset
from api.presentation.web.controllers.schemas.responses import (
    TranslationImageProcessedResponseSchema,
    TranslationResponseSchema,
)
from api.types import ComicID, IssueNumber, Language, TotalCount, TranslationID


class Pagination(BaseModel):
    total: TotalCount
    limit: Limit | None
    offset: Offset | None


class ComicResponseSchema(BaseModel):
    id: ComicID
    number: IssueNumber | None
    publication_date: dt.date
    explain_url: HttpUrl | None
    click_url: HttpUrl | None
    is_interactive: bool
    tags: list[str]
    translation_id: TranslationID  # For transcript getting
    xkcd_url: HttpUrl
    title: str
    tooltip: str
    images: list[TranslationImageProcessedResponseSchema]
    translation_langs: list[Language]

    @classmethod
    def from_dto(cls, dto: ComicResponseDTO) -> "ComicResponseSchema":
        return ComicResponseSchema(
            id=dto.id,
            number=dto.number,
            title=dto.title,
            publication_date=dto.publication_date,
            translation_id=dto.translation_id,
            tooltip=dto.tooltip,
            xkcd_url=dto.xkcd_url,
            explain_url=dto.explain_url,
            click_url=dto.click_url,
            is_interactive=dto.is_interactive,
            tags=dto.tags,
            images=[TranslationImageProcessedResponseSchema.from_dto(img) for img in dto.images],
            translation_langs=dto.translation_langs,
        )


class ComicWTranslationsResponseSchema(ComicResponseSchema):
    translations: Mapping[Language, TranslationResponseSchema]

    @classmethod
    def from_dto(
        cls,
        dto: ComicResponseWTranslationsDTO,
        filter_languages: list[Language] | None = None,
    ) -> "ComicWTranslationsResponseSchema":
        return ComicWTranslationsResponseSchema(
            id=dto.id,
            number=dto.number,
            title=dto.title,
            publication_date=dto.publication_date,
            translation_id=dto.translation_id,
            tooltip=dto.tooltip,
            xkcd_url=dto.xkcd_url,
            explain_url=dto.explain_url,
            click_url=dto.click_url,
            is_interactive=dto.is_interactive,
            tags=dto.tags,
            images=[TranslationImageProcessedResponseSchema.from_dto(img) for img in dto.images],
            translation_langs=dto.translation_langs,
            translations=_prepare_and_filter(dto.translations, filter_languages),
        )


class ComicsWithMetadata(BaseModel):
    meta: Pagination
    data: list[ComicResponseSchema | ComicWTranslationsResponseSchema]


def _prepare_and_filter(
    translations: list[TranslationResponseDTO],
    filter_languages: list[Language] | None = None,
) -> Mapping[Language, TranslationResponseSchema]:
    translation_map = {}
    for tr in translations:
        if not filter_languages or tr.language in filter_languages:
            translation_map.update(TranslationResponseSchema.from_dto(tr))

    return translation_map
