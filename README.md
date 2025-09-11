# Sqirvy LLM Client

A unified Go library and command-line tool for interacting with multiple Large Language Model (LLM) providers. This library provides a way to add a simple AI query to your Go applications.

## Sqirvy LLM Client Library

The `sqirvy-llmclient` library provides a consistent, unified interface for working with AI language models from different providers. It abstracts away provider-specific implementations behind a common `Client` interface, making it easy to switch between different AI models and providers in your Go applications.

### Supported Providers

- **Anthropic**: Claude models (Sonnet, Opus, Haiku)
- **Google**: Gemini models (Pro, Flash)
- **OpenAI**: GPT models

### Key Features

- **Unified Interface**: Single `Client` interface works with all supported providers
- **LangChain Integration**: Built on top of the robust LangChain Go library
- **Model Management**: Centralized model registry with token limits and provider mappings
- **Configuration Options**: Support for temperature, max tokens, custom API keys, and base URLs
- **Error Handling**: Comprehensive error handling with detailed error messages
- **Security**: Request timeouts and input validation

### Quick Start

```go
import "github.com/dmh2000/sqirvy-llmclient"

// Create a client for any supported provider
client, err := sqirvy.NewClient("anthropic")
if err != nil {
    log.Fatal(err)
}
defer client.Close()

// Query the model
ctx := context.Background()
response, err := client.QueryText(
    ctx,
    "You are a helpful assistant",
    []string{"What is the capital of France?"},
    "claude-sonnet-4",
    sqirvy.Options{Temperature: 0.5, MaxTokens: 1000},
)
```

For detailed API documentation, usage examples, and provider-specific information, see [API.md](API.md).

## Sqirvy CLI Tool

The `sqirvy-cli` command-line tool provides an intuitive interface for AI-powered tasks from the terminal. It's designed for pipeline usage, making it easy to integrate AI capabilities into shell scripts and command workflows.

### Features

- **Multiple Commands**: Specialized commands for different AI tasks
  - `query` - General purpose AI queries (default command)
  - `plan` - Generate plans and strategies
  - `code` - Generate source code
  - `review` - Perform code reviews
- **Pipeline Support**: Reads from stdin, files, and URLs; outputs to stdout
- **Flexible Input**: Supports multiple input sources simultaneously
- **Model Selection**: Choose from any supported model with `-m/--model` flag
- **Configuration**: YAML configuration file support and environment variables
- **Web Scraping**: Built-in URL content extraction for AI analysis

### Installation

```bash
# Build from source
make build

# Binary will be created at cmd/bin/sqirvy-cli
```

### Quick Examples

```bash
# Basic query (query is the default command)
echo "What is Go?" | sqirvy-cli

# Generate a plan
sqirvy-cli plan -m claude-sonnet-4 "Build a web application"

# Code review
sqirvy-cli review -m gemini-2.5-flash main.go

# Generate code
echo "Create a REST API endpoint" | sqirvy-cli code > api.go

# Use with files and URLs
sqirvy-cli query -m gpt-5 file1.go file2.go https://example.com

# Pipeline usage
cat requirements.txt | sqirvy-cli plan | sqirvy-cli code > implementation.go
```

### Configuration

Create a configuration file at `~/.config/sqirvy-cli/config.yaml`:

```yaml
model: claude-3-5-haiku
temperature: 0.25
```

Set required environment variables:

- `ANTHROPIC_API_KEY` - For Claude models
- `GEMINI_API_KEY` - For Gemini models
- `OPENAI_API_KEY` - For OpenAI models

### Commands

- **sqirvy-cli query** - Send arbitrary queries to the LLM
- **sqirvy-cli plan** - Generate plans, strategies, and architectural designs
- **sqirvy-cli code** - Generate source code and implementations
- **sqirvy-cli review** - Perform code reviews and analysis

All commands support:

- `-m/--model` - Specify the AI model to use
- `-t/--temperature` - Control response randomness (0.0-1.0)
- Input from stdin, files, and URLs
- Output to stdout for pipeline usage

### Enhanced AI Prompts

The CLI tool includes comprehensive, professionally-crafted prompts designed to deliver enterprise-quality AI assistance:

#### Available Prompt Templates

Located in `cmd/sqirvy-cli/cmd/prompts/`:

- **`query.md`** - Expert general-purpose AI assistant with advanced conversation capabilities, educational support, creative collaboration, and structured analytical responses
- **`plan.md`** - Comprehensive software architecture and design specification generator for creating detailed, production-ready system blueprints
- **`code.md`** - Expert code generation assistant focused on security, performance, maintainability, and modern development practices
- **`review.md`** - Thorough code review framework covering bugs, security, performance, design patterns, and best practices
- **`ethics.md`** - Comprehensive ethical AI framework establishing principles for responsible, beneficial, and trustworthy AI assistance

#### Prompt Features

- **Production-Quality Standards**: Enterprise-level guidelines for professional AI assistance
- **Security-First Approach**: Built-in security best practices and vulnerability prevention
- **Comprehensive Coverage**: Detailed frameworks covering all aspects of AI assistance
- **Ethical Foundation**: Strong ethical principles ensuring responsible AI usage
- **Modern Development Practices**: Latest industry standards and methodologies
- **Structured Methodologies**: Clear, actionable guidelines for consistent quality

These enhanced prompts ensure that the CLI tool delivers professional-grade AI assistance suitable for production environments, educational use, and enterprise applications.

## Testing

The project includes comprehensive testing at multiple levels to ensure reliability and functionality.

### Library Tests

**Location**: Root directory  
**Command**: `make test` or `go test -v -timeout 2m .`

**Coverage**:
- Unit tests for each AI provider client (`*_test.go`)
- Client interface validation
- Model registry functionality
- Error handling and edge cases
- Configuration and option handling

**Test Structure**:
- `anthropic_test.go` - Anthropic Claude client tests
- `gemini_test.go` - Google Gemini client tests  
- `openai_test.go` - OpenAI client tests
- `models_test.go` - Model registry and mapping tests
- `client_test.go` - Core client interface tests

### CLI Integration Tests

**Location**: `cmd/sqirvy-cli/`  
**Command**: `./test.sh`

**Coverage**:
- End-to-end CLI command testing
- All command types (query, plan, code, review)
- Multiple AI model integration
- Input/output pipeline validation
- Configuration file handling
- Error condition testing

**Test Outputs**: 
- Test results stored in `cmd/sqirvy-cli/test/` directory
- Includes sample outputs for validation
- Performance and response quality assessment

### Running Tests

```bash
# Run all library tests
make test

# Run CLI integration tests
cd cmd/sqirvy-cli && ./test.sh

# Run specific provider tests
go test -v -run TestAnthropic .
go test -v -run TestGemini .
go test -v -run TestOpenAI .

# Run tests with coverage
go test -v -cover .
```

### Test Requirements

**Environment Variables**: Tests require valid API keys for full integration testing:
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY` 
- `OPENAI_API_KEY`

**Network Access**: Integration tests make real API calls to validate provider functionality

**Timeout Handling**: Tests include appropriate timeouts (2 minutes) for network operations

The testing suite ensures the library and CLI tool work correctly with all supported AI providers and handle various input scenarios, error conditions, and configuration options.

## License

Licensed under the terms specified in the LICENSE file.
