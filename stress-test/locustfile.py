from locust import HttpUser, task, between
import random
import uuid
import string

class BookUser(HttpUser):
	wait_time = between(0.5, 1)
	books_created = []

	def on_start(self):
		self.client.timeout = 2

	@task(10)
	def create_book(self):
		book = {
			"name": f"book-{uuid.uuid4()}",
			"price": round(random.uniform(5, 150), 2),
			"author": f"Author-{uuid.uuid4()}",
			"releaseDate": "2020-01-01",
			"pages": random.randint(100, 500)
		}

		with self.client.post(
			"/books",
			json=book,
			headers={"Content-Type": "application/json"},
			timeout=self.client.timeout,
			catch_response=True
		) as response:
				if response.status_code == 201 and response.headers['Location'] is not None:
					self.books_created.append(response.headers['Location'])
					response.success()
				elif response.elapsed.total_seconds() > self.client.timeout:
					response.failure("Request timed out")
				else:
					response.failure(f"Unexpected response: {response.status_code}")

	@task(1)
	def insert_invalid_request_format(self):
		invalid_books = [
			{
				"name": f"book-{uuid.uuid4()}",
				"price": "invalid_price",  # Invalid price format
				"author": "Author Name",
				"releaseDate": "2020-01-01",
				"pages": random.randint(100, 500)
			},
			{
				"name": f"book-{uuid.uuid4()}",
				"price": 19.99,
				"author": "Author Name",
				"releaseDate": "2020-01-01",
				"pages": "invalid_pages"  # Invalid pages format
			},
			{
				"name": f"book-{uuid.uuid4()}",
				"price": 19.99,
				"author": 123, # Invalid author format
				"releaseDate": "1925-04-10", # Invalid date format
				"pages": random.randint(100, 500),
			},
		]

		for book in invalid_books:
			with self.client.rename_request("/books-invalid"):
				with self.client.post(
						"/books",
						json=book,
						headers={"Content-Type": "application/json"},
						timeout=self.client.timeout,
						catch_response=True
					) as response:
						if response.status_code == 422:
							response.success()
						elif response.elapsed.total_seconds() > self.client.timeout:
							response.failure("Request timed out")

	@task(3)
	def search_books(self):
		with self.client.rename_request("/books?s=[search]"):
			search = ''.join(random.choices(string.ascii_uppercase, k=random.randint(3, 20)))
			with self.client.get(f"/books?s={search}", timeout=self.client.timeout, catch_response=True) as response:
				if response.status_code == 200:
					response.success()
				elif response.elapsed.total_seconds() > self.client.timeout:
					response.failure("Request timed out")
				else:
					response.failure(f"Unexpected response: {response.status_code}")

	@task(3)
	def get_created_book(self):
		if len(self.books_created) > 0:
			book_url = random.choice(self.books_created)
			with self.client.rename_request("/books/[id]"):
				with self.client.get(book_url, timeout=self.client.timeout, catch_response=True) as response:
					if response.status_code == 200:
						response.success()
					elif response.elapsed.total_seconds() > self.client.timeout:
						response.failure("Request timed out")
					else:
						response.failure(f"Unexpected response: {response.status_code}")
		else:
			print("No books have been created yet.")
