from locust import HttpUser, task, between


class UserBehavior(HttpUser):
    wait_time = between(1, 3)  # время ожидания между запросами от 1 до 3 секунд

    @task
    def ad(self):
        self.client.get("/advertisements/")  # делаем GET-запрос к корневому пути

    @task(2)  # второй метод будет запускаться в 2 раза чаще
    def ad_with_comment(self):
        self.client.get("/advertisements/comments/")  # делаем GET-запрос к /about
