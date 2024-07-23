from data_source import DataSource

class SourceFetcher:
    def __init__ (self):
        self.sources = []
    
    def add_source(self, source):
        if isinstance(source, DataSource):
            self.sources.append(source)
    
    def fetch_source(self, identifier):
        results_sources = []
        for source in self.sources:
            results = source.get_profile()
            results_sources.append(results)
                
            
        if not(len(results_sources)): 
            return {
                    'status': 404,
                    'error': 'No se han encontrado resultados en ninguna fuente.'
            }
        print(results_sources)
        combined_results = {}
        for result in results_sources:
            for key, value in result.items():
                if key in combined_results and isinstance(value, list) and isinstance(combined_results[key], list):
                    combined_results[key].extend(value)
                else:
                    combined_results[key] = value
            
        return combined_results
                
            