# config.py

knowledge_sources = [
    {
        "name": "METRO",
        "international": True,
        "url": "https://metro.co.uk/news/",
        "title_class": "article__title",
        "resume_class": "article__title",
        "body_class": "article__content",
        "index_path":"./indexes/metro_document_index.json",
        "vector_index_path":"./vector_indexes/metro_vector_index.faiss"
    },
    {
        "name": "The daily mail",
        "international": True,
        "url": "https://www.dailymail.co.uk/",
        "title_class": "headline--chWWs",
        "resume_class": "headline--chWWs",
        "body_class": "mol-para-with-font",
        "index_path":"./indexes/thedailymail_document_index.json",
        "vector_index_path":"./vector_indexes/thedailymail_vector_index.faiss"
    },
    {
        "name": "El País",
        "international": False,
        "url": "https://elpais.com",
        "title_class": "a_t",
        "resume_class": "a_st",
        "body_class": "a_c clearfix",
        "index_path":"./indexes/elpais_document_index.json",
        "vector_index_path":"./vector_indexes/elpais_vector_index.faiss"
    },
    {
        "name": "El Mundo",
        "international": False,
        "url": "https://elmundo.es", 
        "title_class": "ue-c-article__headline js-headline",
        "resume_class": "ue-c-article__standfirst",
        "body_class": "ue-c-article__body",
        "index_path":"./indexes/elmundo_document_index.json",
        "vector_index_path":"./vector_indexes/elmundo_vector_index.faiss"
    },
    {
        "name": "La Vanguardia",
        "international": False,
        "url": "https://www.lavanguardia.com/",
        "title_class": "title",
        "resume_class": "epigraph",
        "body_class": "article-modules",
        "index_path":"./indexes/lavanguardia_document_index.json",
        "vector_index_path":"./vector_indexes/lavanguardia_vector_index.faiss"
    },
    {
        "name": "El Español",
        "international": False,
        "url": "https://www.elespanol.com/",
        "title_class": "article-header__heading article-header__heading--s3",
        "resume_class": "article-header__subheading",
        "body_class": "article-body__content",
        "index_path":"./indexes/elespanol_document_index.json",
        "vector_index_path":"./vector_indexes/elespanol_vector_index.faiss"
    },
    {
        "name": "El Periódico De Catluña",
        "international": False,
        "url": "https://www.elperiodico.com/",
        "title_class": "ft-title ft-helper-spacer-b-xs ft-helper-fontSize-heading-M",
        "resume_class": "ft-mol-subtitle ft-mol-subtitle--listSimple ft-helper-fontColor-quaternary",
        "body_class": "ft-helper-closenews-all",
        "index_path":"./indexes/elperiodicodecatluna_document_index.json",
        "vector_index_path":"./vector_indexes/elperiodicodecatluna_vector_index.faiss"
    },
    {
        "name": "Eldiario.Es",
        "international": False,
        "url": "https://www.eldiario.es/",
        "title_class": "title",
        "resume_class": "footer",
        "body_class": "second-col",
        "index_path":"./indexes/eldiario.es_document_index.json",
        "vector_index_path":"./vector_indexes/eldiario.es_vector_index.faiss"
    },
    {
        "name": "La Razón",
        "international": False,
        "url": "https://www.larazon.es/",
        "title_class": "article-main__title",
        "resume_class": "article-main__description",
        "body_class": "article-main__content",
        "index_path":"./indexes/larazon_document_index.json",
        "vector_index_path":"./vector_indexes/larazon_vector_index.faiss"
    },
    {
        "name": "20 Minutos",
        "international": False,
        "url": "https://www.20minutos.es/",
        "title_class": "article-title",
        "resume_class": "article-intro trk-relacionada-bolos",
        "body_class": "article-body",
        "index_path":"./indexes/20minutos_document_index.json",
        "vector_index_path":"./vector_indexes/20minutos_vector_index.faiss"
    },
    {
        "name": "Libertad Digital",
        "international": False,
        "url": "https://www.libertaddigital.com/",
        "title_class": "heading",
        "resume_class": "lede",
        "body_class": "body ",
        "index_path":"./indexes/libertaddigital_document_index.json",
        "vector_index_path":"./vector_indexes/libertaddigital_vector_index.faiss"
    },
    {
        "name": "Europa Press",
        "international": False,
        "url": "https://www.europapress.es/",
        "title_class": "titular",
        "resume_class": "div_relacionadas",
        "body_class": "NormalTextoNoticia",
        "index_path":"./indexes/europapress_document_index.json",
        "vector_index_path":"./vector_indexes/europapress_vector_index.faiss"
    },
    {
        "name": "Diario De Sevilla",
        "international": False,
        "url": "https://www.diariodesevilla.es/",
        "title_class": "headline-atom B-700-500-100-N B-850-500-150-N--md",
        "resume_class": "subtitle-atom B-500-400-300-N B-525-400-300-N--md mb-3_5",
        "body_class": "bbnx-body prometeo-hideable two-columns-default-width",
        "index_path":"./indexes/diariodesevilla_document_index.json",
        "vector_index_path":"./vector_indexes/diariodesevilla_vector_index.faiss"
    },
    {
        "name": "La Voz De Galicia",
        "international": False,
        "url": "https://www.lavozdegalicia.es/",
        "title_class": "headline mg-b-2",
        "resume_class": "subtitle t-bld",
        "body_class": "col sz-dk-67 txt-blk",
        "index_path":"./indexes/lavozdegalicia_document_index.json",
        "vector_index_path":"./vector_indexes/lavozdegalicia_vector_index.faiss"
    },
    {
        "name": "Huffington Post",
        "international": False,
        "url": "https://www.huffingtonpost.es/",
        "title_class": "c-detail__title",
        "resume_class": "c-detail__subtitle",
        "body_class": "c-detail__body",
        "index_path":"./indexes/huffingtonpost_document_index.json",
        "vector_index_path":"./vector_indexes/huffingtonpost_vector_index.faiss"
    },
    {
        "name": "Público",
        "international": False,
        "url": "https://www.publico.es/",
        "title_class": "article-title text-balance desktop:text-pretty leading-tight mb-7 desktop:mb-5 font-serif text-xl8 desktop:text-xxxl",
        "resume_class": "text-base desktop:text-xl text-pretty text-neutral-gray-800 dark:text-cold-gray-200 mb-5 desktop:mb-7 [&_ul]:list-disc desktop:[&_ul]:ml-3 [&_li]:marker:text-publico [&_li]:mb-2 [&_a]:text-link-normal dark:[&_a]:text-link-dark [&_a]:underline [&_a:hover]:text-link-hover [&_a:hover]:no-underline [&_a:hover]:dark:text-link-dark-hover",
        "body_class": "body-modules w-full",
        "index_path":"./indexes/publico_document_index.json",
        "vector_index_path":"./vector_indexes/publico_vector_index.faiss"
    },
    {
        "name": "The Guardian",
        "international": True,
        "url": "https://www.theguardian.com/europe",
        "title_class": "dcr-u0152o",
        "resume_class": "dcr-1b20i6h",
        "body_class": "article-body-commercial-selector article-body-viewer-selector dcr-11jq3zt",
        "index_path":"./indexes/theguardian_document_index.json",
        "vector_index_path":"./vector_indexes/theguardian_vector_index.faiss"
    },
    {
        "name": "BBC",
        "international": True,
        "url": "https://www.bbc.com/news",
        "title_class": "sc-f98b1ad2-0 dfvxux",
        "resume_class": "sc-f98b1ad2-0 dfvxux",
        "body_class": "sc-3b6b161a-0 dEGcKf",
        "index_path":"./indexes/bbc_document_index.json",
        "vector_index_path":"./vector_indexes/bbc_vector_index.faiss"
    },
    {
        "name": "CBS",
        "international": True,
        "url": "https://www.cbsnews.com/",
        "title_class": "content__title",
        "resume_class": "content__title",
        "body_class": "content__body",
        "index_path":"./indexes/cbs_document_index.json",
        "vector_index_path":"./vector_indexes/cbs_vector_index.faiss"
    },
    {
        "name": "GB news",
        "international": True,
        "url": "https://www.gbnews.com/",
        "title_class": "widget__headline h1",
        "resume_class": "widget__subheadline-text h2",
        "body_class": "body-description",
        "index_path":"./indexes/gbnews_document_index.json",
        "vector_index_path":"./vector_indexes/gbnews_vector_index.faiss"
    },
    {
        "name": "Huffpost",
        "international": True,
        "url": "https://www.huffpost.com/",
        "title_class": "headline",
        "resume_class": "dek",
        "body_class": "primary-cli cli cli-text",
        "index_path":"./indexes/huffpost_document_index.json",
        "vector_index_path":"./vector_indexes/huffpost_vector_index.faiss"
    },
]
