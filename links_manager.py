class LinksManager:
    _instance = None
    _domain_name = None
    sitemap_urls = []
    links_url = []

    @classmethod
    def initialize(cls, domain_name):
        if cls._instance is None:
            cls._instance = cls()
            cls._domain_name = domain_name
        return cls._instance

    @classmethod
    def add_sitemap_urls(cls, url):
        cls.links_url.append(url)

    @classmethod
    def add_link(cls, url):
        cls.links_url.append(url)

    @classmethod
    def get_identified_links(cls):
        return cls.links_url
    
    @classmethod
    def reset_links(cls):
        cls._instance = None
        cls._domain_name = None
        cls.sitemap_urls = []
        cls.links_url = []