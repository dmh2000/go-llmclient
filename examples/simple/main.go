package main

import (
	"context"
	"fmt"

	sqirvy "github.com/dmh2000/go-llmclient"
)

// This example is an example of a simple query where the system prompt is provided by the user
func main() {

	for _, model := range sqirvy.GetModelList() {
		fmt.Println(model)
	}

	client, err := sqirvy.NewClient("anthropic")
	if err != nil {
		fmt.Println(err)
		return
	}
	system := "you are a helpful assistant"
	prompts := []string{
		"Write a poem about a happy carrot",
		"Write a poem about a sad carrot",
	}
	resp, err := client.QueryText(context.Background(), system, prompts, "claude-sonnet-4-20250514", sqirvy.Options{})
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(resp)
}
