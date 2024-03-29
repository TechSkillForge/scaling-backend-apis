package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type Book struct {
	ID          uuid.UUID `json:"id"`
	Name        string    `json:"name"`
	Price       float64   `json:"price"`
	Author      string    `json:"author"`
	ReleaseDate string    `json:"releaseDate"`
	Pages       int       `json:"pages"`
}

func main() {
	r := gin.Default()

	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	r.POST("/books", createBookHandler())
	r.GET("/books/:id", getBookByIDHandler())
	r.GET("/books", searchBooksHandler())
	r.GET("/book-count", countBooksHandler())

	r.Run(":8080")
}

func createBookHandler() gin.HandlerFunc {
	return func(c *gin.Context) {
		// TODO: Implement the create book handler
		c.Status(http.StatusCreated)
	}
}

func getBookByIDHandler() gin.HandlerFunc {
	return func(c *gin.Context) {
		// TODO: Implement the get book by ID handler

		c.JSON(http.StatusOK, Book{})
	}
}

func searchBooksHandler() gin.HandlerFunc {
	return func(c *gin.Context) {
		// TODO: Implement the search books handler
		c.JSON(http.StatusOK, []Book{})
	}
}

func countBooksHandler() gin.HandlerFunc {
	return func(c *gin.Context) {
		// TODO: Implement the count books handler
		c.JSON(http.StatusOK, gin.H{"count": 0})
	}
}
