package main

import (
	"context"
	"fmt"

	sqirvy "github.com/dmh2000/go-llmclient"
)

var system = `You are an expert in ai and large language models who it teaching a junior software developer.
answer the following questions in one or two paragraphs each.`

var prompt1 = "Describe in one paragraph how the embeddings are generated."
var prompt2 = "What does the positional encoding phase do to the embeddings"
var prompt3 = "What does the attention phase do"
var prompt4 = "What does the feed forward neural network phase do."

// This is an example of a multi-step query
func main() {

	for _, model := range sqirvy.GetModelList() {
		fmt.Println(model)
	}

	client, err := sqirvy.NewClient("anthropic")
	if err != nil {
		fmt.Println(err)
		return
	}

	var conversation []string
	var resp string

	// Step 1
	conversation = append(conversation, prompt1)
	resp, err = client.QueryText(context.Background(), system, conversation, "gemini-2.5-flash", sqirvy.Options{})
	if err != nil {
		fmt.Println(err)
		return
	}
	conversation = append(conversation, resp)

	// Step 2
	conversation = append(conversation, prompt2)
	resp, err = client.QueryText(context.Background(), system, conversation, "gemini-2.5-flash", sqirvy.Options{})
	if err != nil {
		fmt.Println(err)
		return
	}
	conversation = append(conversation, resp)

	// Step 3
	conversation = append(conversation, prompt3)
	resp, err = client.QueryText(context.Background(), system, conversation, "gemini-2.5-flash", sqirvy.Options{})
	if err != nil {
		fmt.Println(err)
		return
	}
	conversation = append(conversation, resp)

	// Step 4
	conversation = append(conversation, prompt4)
	resp, err = client.QueryText(context.Background(), system, conversation, "gemini-2.5-flash", sqirvy.Options{})
	if err != nil {
		fmt.Println(err)
		return
	}
	conversation = append(conversation, resp)

	for _, v := range conversation {
		fmt.Println(v)
	}
}
