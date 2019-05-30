from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

   
    def login(self):
        response = self.client.post(
        url="/auth/login", 
        data=
            {"username":"deliverymuch", "password":"delivery123"}
        )
        body = response.json()
        self.token = "Bearer " + body['access_token']
        #print("Token:", self.token)

    @task(2)
    def companies(self):
        self.client.get(
            url = "/companies",
            headers={
                    "Authorization": self.token
            },
        )

    @task(1)
    def companiesOrders(self):
        self.client.get(
            url = "/companies/11e7df2c-9aef-a80e-85d8-02ef04cb3aba/orders",
            headers={
                    "Authorization": self.token
            },
        )   

class WebsiteUser(HttpLocust):
    """
    Locust user class that does requests to the locust web server running on localhost
    """
    host = "https://bffres.deliverymu.ch"
    min_wait = 2000
    max_wait = 5000
    task_set = UserBehavior   