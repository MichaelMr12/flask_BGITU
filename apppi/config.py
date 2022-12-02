import os


class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'fasfjkdma;oiutrjf;wmgfoiewu4hjnlkhgierioj'
