// package go_llmclient provides model management functionality for AI language models.
//
// This file contains model-to-provider mappings and utility functions for
// working with different AI models across supported providers.
package go_llmclient

import (
	"fmt"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

var modelAlias = map[string]string{
	"claude-sonnet-4":  "claude-sonnet-4-5-20250929",
	"claude-opus-4-1":  "claude-opus-4-1-20250805",
	"claude-3-5-haiku": "claude-3-5-haiku-20241022",
}

// Supported AI providers
const (
	Anthropic string = "anthropic" // Anthropic's Claude models
	Gemini    string = "gemini"    // Google's Gemini models
	OpenAI    string = "openai"    // OpenAI's GPT models
)

// modelRegistry consolidates provider and token information for each model
// This helps ensure consistency between provider and token information.
// These mappings are essential for the QueryText functions to route requests
// to the appropriate client.

// ModelInfo holds information about a specific model
type ModelInfo struct {
	Provider        string
	MaxOutputTokens int64
}

// modelRegistry is the single source of truth for model information
var modelRegistry = map[string]ModelInfo{
	// anthropic models
	"claude-sonnet-4-5-20250929": {Provider: Anthropic, MaxOutputTokens: 64000},
	"claude-opus-4-1-20250805":   {Provider: Anthropic, MaxOutputTokens: 32000},
	"claude-3-5-haiku-20241022":  {Provider: Anthropic, MaxOutputTokens: 8096},
	// google gemini models
	"gemini-2.5-pro":   {Provider: Gemini, MaxOutputTokens: 64000},
	"gemini-2.5-flash": {Provider: Gemini, MaxOutputTokens: 64000},
	// openai models
	"gpt-5":      {Provider: OpenAI, MaxOutputTokens: 64000},
	"gpt-5-mini": {Provider: OpenAI, MaxOutputTokens: 64000},
}

// ModelToMaxTokens maps model names to their maximum token limits.
// If a model is not in this map, MAX_TOKENS_DEFAULT will be used.
// MAX_TOKENS_DEFAULT is defined in client.go
// This map is maintained for backward compatibility
var modelToMaxOutputTokens = map[string]int64{}

// CustomModelConfig represents the structure of the custom models configuration file
type CustomModelConfig struct {
	Models []CustomModel `yaml:"models"`
}

// CustomModel represents a single custom model configuration
type CustomModel struct {
	Name            string `yaml:"name"`
	Provider        string `yaml:"provider"`
	MaxOutputTokens int64  `yaml:"max_output_tokens"`
}

// getConfigPath searches for a custom models configuration file in the following order:
// 1. Environment variable: LLMCLIENT_MODELS_CONFIG
// 2. Current directory: ./llmclient-models.yaml
// 3. User home: ~/.config/llmclient/models.yaml
func getConfigPath() string {
	// Check environment variable
	if configPath := os.Getenv("LLMCLIENT_MODELS_CONFIG"); configPath != "" {
		if _, err := os.Stat(configPath); err == nil {
			return configPath
		}
	}

	// Check current directory
	if _, err := os.Stat("./llmclient-models.yaml"); err == nil {
		return "./llmclient-models.yaml"
	}

	// Check user home config directory
	if homeDir, err := os.UserHomeDir(); err == nil {
		configPath := filepath.Join(homeDir, ".config", "llmclient", "models.yaml")
		if _, err := os.Stat(configPath); err == nil {
			return configPath
		}
	}

	return ""
}

// LoadCustomModels loads custom model configurations from a YAML file
// and merges them into the modelRegistry. Built-in models cannot be overridden.
// Returns an error if the file cannot be read or parsed, or if any model has an invalid provider.
func LoadCustomModels(configPath string) error {
	data, err := os.ReadFile(configPath)
	if err != nil {
		return fmt.Errorf("failed to read config file: %w", err)
	}

	var config CustomModelConfig
	if err := yaml.Unmarshal(data, &config); err != nil {
		return fmt.Errorf("failed to parse config file: %w", err)
	}

	// Validate and add custom models
	for _, model := range config.Models {
		// Validate provider
		if model.Provider != Anthropic && model.Provider != Gemini && model.Provider != OpenAI {
			return fmt.Errorf("invalid provider '%s' for model '%s': must be one of %s, %s, or %s",
				model.Provider, model.Name, Anthropic, Gemini, OpenAI)
		}

		// Don't allow overriding built-in models
		if _, exists := modelRegistry[model.Name]; exists {
			continue
		}

		// Add custom model to registry
		modelRegistry[model.Name] = ModelInfo{
			Provider:        model.Provider,
			MaxOutputTokens: model.MaxOutputTokens,
		}
	}

	return nil
}

// Initialize modelToMaxTokens from modelRegistry for backward compatibility
func init() {
	// First, populate backward compatibility map from built-in models
	for model, info := range modelRegistry {
		modelToMaxOutputTokens[model] = info.MaxOutputTokens
	}

	// Load custom models if config exists
	if configPath := getConfigPath(); configPath != "" {
		// Ignore errors to allow app to run with defaults
		_ = LoadCustomModels(configPath)

		// Update backward compatibility map with any newly added models
		for model, info := range modelRegistry {
			if _, exists := modelToMaxOutputTokens[model]; !exists {
				modelToMaxOutputTokens[model] = info.MaxOutputTokens
			}
		}
	}
}

// GetModelAlias returns the standardized model name for a given alias.
// This is used in cmd/sqirvy-cli to validate the model command line argument
// The model uses the input value unless there is an alias
func GetModelAlias(model string) string {
	if alias, ok := modelAlias[model]; ok {
		return alias
	}
	return model
}

// GetModelList returns a list of all supported model names
func GetModelList() []string {
	var models []string
	for model := range modelRegistry {
		models = append(models, model)
	}
	return models
}

type ModelProvider struct {
	Model    string
	Provider string
}

func GetModelProviderList() []ModelProvider {
	var mp []ModelProvider
	for model, info := range modelRegistry {
		mp = append(mp, ModelProvider{Model: model, Provider: info.Provider})
	}
	return mp
}

// GetProviderName returns the provider name for a given model identifier.
// Returns an error if the model is not recognized.
func GetProviderName(model string) (string, error) {
	if info, ok := modelRegistry[model]; ok {
		return info.Provider, nil
	}
	return "", fmt.Errorf("unrecognized model: %s", model)
}

// GetMaxTokensWithError returns the maximum token limit for a given model identifier
// along with an error if the model is not recognized.
// This function provides more detailed error reporting compared to GetMaxTokens.
func GetMaxTokensWithError(model string) (int64, error) {
	if info, ok := modelRegistry[model]; ok {
		return info.MaxOutputTokens, nil
	}
	return MAX_TOKENS_DEFAULT, fmt.Errorf("unrecognized model: %s, using default token limit", model)
}

// GetMaxTokens returns the maximum token limit for a given model identifier.
// Returns MAX_TOKENS_DEFAULT if the model is not in ModelToMaxTokens.
// This function maintains backward compatibility with existing code.
func GetMaxTokens(model string) int64 {
	tokens, _ := GetMaxTokensWithError(model)
	return tokens
}
