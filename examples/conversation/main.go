package main

import (
	"context"
	"fmt"

	llmclient "github.com/dmh2000/go-llmclient"
)

var system = `You are an expert in ai and large language models who it teaching a junior software developer.
answer the following questions in one or two paragraphs each. the output should be in markdown format. Create a 
markdown level 2 heading for each prompt. Don't repeat headings from the prompts. don't repeat the prompts.`

var prompt1 = "\n **HOW ARE THE INITIAL EMBEDDINGS GENERATED?**\n"
var prompt2 = "\n **WHAT DOES THE POSITIONAL ENCODING PHASE DO TO THE EMBEDDINGS?**\n"
var prompt3 = "\n **WHAT DOES THE ATTENTION PHASE DO?**\n"
var prompt4 = "\n **WHAT DOES THE FEED FORWARD NEURAL NETWORK PHASE DO?**\n"

// This is an example of a multi-step query
func main() {

	provider := "gemini"
	client, err := llmclient.NewClient(provider)
	if err != nil {
		fmt.Println(err)
		return
	}
	model := "gemini-2.5-flash"
	fmt.Printf("Using provider: %s model: %s\n", provider, model)

	var conversation []string
	var resp string

	// Step 1
	conversation = append(conversation, prompt1)
	resp, err = client.QueryText(context.Background(), system, conversation, model, llmclient.Options{})
	if err != nil {
		fmt.Println(err)
		return
	}
	conversation = append(conversation, resp)

	// Step 2
	conversation = append(conversation, prompt2)
	resp, err = client.QueryText(context.Background(), system, conversation, model, llmclient.Options{})
	if err != nil {
		fmt.Println(err)
		return
	}
	conversation = append(conversation, resp)

	// Step 3
	conversation = append(conversation, prompt3)
	resp, err = client.QueryText(context.Background(), system, conversation, model, llmclient.Options{})
	if err != nil {
		fmt.Println(err)
		return
	}
	conversation = append(conversation, resp)

	// Step 4
	conversation = append(conversation, prompt4)
	resp, err = client.QueryText(context.Background(), system, conversation, model, llmclient.Options{})
	if err != nil {
		fmt.Println(err)
		return
	}
	conversation = append(conversation, resp)

	for _, v := range conversation {
		fmt.Println(v)
		fmt.Println()
	}
}
