class HealthCheckResult():
    
    def __init__(self, health_check_destination_results, successful, error):
        self.health_check_destination_results = []
        self.successful = False
        self.error = None
        
        if health_check_destination_results is not None:
            for result in health_check_destination_results:
                self.addHealthCheckDestinationResult(result)

        if successful is not None:
            self.successful = successful
            
        if error is not None:
            self.error = error
    
    def addHealthCheckDestinationResult(self, health_check_destination_result):
        self.health_check_destination_results.append(health_check_destination_result)
        
    def setHealthCheckDestinationResults(self, health_check_destination_results):
        self.health_check_destination_results = health_check_destination_results
    
    def getHealthCheckDestinationResults(self):
        return self.health_check_destination_results
    
    def setSuccessful(self, successful):
        this.successful = successful
        
    def isSuccessful(self):
        return self.successful

    def setError(self, error):
        self.error = error
        
    def getError(self):
        return self.error