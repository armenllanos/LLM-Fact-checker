
import configparser


class Settings():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("appsettings.ini")
        app = config["app"]
        self.media_source_number = app.getint("media_source_number")
        self.app_name = app.get("app_name")   
        self.content_validation_prompt = app.get("content_validation_prompt")
        self.is_global_prompt = app.get("is_global_prompt")
        self.claim_extractor_prompt = app.get("claim_extractor_prompt")
        self.international_response = app.get("international_response")
        self.min_news_false_score = app.getfloat("min_news_false_score")
        self.min_news_true_score = app.getfloat("min_news_true_score")
        self.max_workers_secciones = app.getint("max_workers_secciones")
        self.number_news_per_source = app.getint("number_news_per_source")
        self.min_false_prop = app.getfloat("min_false_prop")
        self.min_true_prop = app.getfloat("min_true_prop")
        self.min_cos_dist = app.getfloat("min_cos_dist")
        self.min_semantic_score = app.getfloat("min_semantic_score")
        self.min_content_score = app.getfloat("min_content_score")
        self.max_workers_principal = app.get("max_workers_principal")
        self.embedding_model = app.get("embedding_model")
        self.search_engine = app.get("search_engine")
        self.wait_time_curtesy = app.getint("wait_time_curtesy")
        self.wait_time_between_calls = app.getint("wait_time_between_calls")
        self.api_model_name = app.get("api_model_name")
        self.api_url = app.get("api_url")
        self.translation_model_name = app.get("translation_model_name")
        self.semantic_model_name = app.get("semantic_model_name")
        self.gemma_api_key = app.get("gemma_api_key")
        self.gemma_model_name = app.get("gemma_model_name")
        self.min_claim_score = app.getfloat("min_claim_score")
        self.min_true_prop = app.getfloat("min_true_prop")
        self.min_news_score = app.getfloat("min_news_score")
        self.min_prop = app.getfloat("min_prop")


