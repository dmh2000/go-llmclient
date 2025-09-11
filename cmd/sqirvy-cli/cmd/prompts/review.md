```prompt
# Comprehensive Code Review Guidelines

Conduct a thorough code review examining the following critical categories with detailed analysis:

## Primary Review Categories

### 1. Bugs and Logic Issues
- Runtime errors, null pointer exceptions, index out of bounds
- Logic errors that could cause incorrect behavior
- Infinite loops or recursive calls without proper termination
- Race conditions and concurrency issues
- Memory leaks or resource management problems
- Error handling gaps or improper exception management
- Edge cases not properly handled (empty inputs, boundary values)

### 2. Security Vulnerabilities
- Input validation and sanitization issues
- SQL injection, XSS, or other injection vulnerabilities
- Authentication and authorization flaws
- Sensitive data exposure (hardcoded secrets, logging sensitive info)
- Insecure cryptographic practices
- Path traversal vulnerabilities
- Improper session management
- CSRF vulnerabilities
- Dependency vulnerabilities

### 3. Performance Issues
- Inefficient algorithms (O(n²) when O(n log n) possible)
- Database query optimization opportunities
- Memory usage inefficiencies
- Unnecessary object creation or string concatenation
- I/O operations that could be batched or cached
- Network calls that could be optimized
- Resource-intensive operations in tight loops
- Missing indexing or caching strategies

### 4. Code Quality and Design
- SOLID principles adherence
- Design patterns appropriateness
- Separation of concerns
- Code duplication (DRY principle violations)
- Function/method length and complexity
- Class cohesion and coupling
- Dependency injection opportunities
- Interface design and abstraction levels

### 5. Style and Language Idioms
- Language-specific best practices and conventions
- Consistent naming conventions (camelCase, snake_case, etc.)
- Code formatting and indentation consistency
- Proper use of language features (generics, lambdas, etc.)
- Framework-specific conventions
- Import organization and unused imports
- Variable and function naming clarity

## Additional Review Criteria

### Code Maintainability
- Code readability and self-documentation
- Comment quality and necessity
- Function and variable naming descriptiveness
- Code organization and structure
- Documentation completeness
- Test coverage and quality

### Architecture and Design
- Modularity and component boundaries
- Scalability considerations
- Configuration management
- Logging and monitoring integration
- Error handling consistency
- API design quality

### Best Practices Compliance
- Industry standards adherence
- Framework-specific guidelines
- Team coding standards
- Version control practices
- Dependency management

## Review Instructions

- **Precision**: Include exact filename and line number for each finding
- **Context**: Consider the broader codebase architecture and patterns
- **Severity**: Categorize findings as Critical, High, Medium, or Low priority
- **Actionability**: Provide specific, actionable recommendations
- **Balance**: Acknowledge well-written code alongside issues
- **External Dependencies**: Assume imported/referenced external packages are secure and functional

## Output Format Requirements

- Use markdown formatting for clear presentation
- Group findings by category and severity
- Provide code snippets for context when helpful
- Include rationale for each recommendation
- Summarize overall code quality assessment

# Enhanced Markdown Template:

    ```markdown
    # Code Review Report

    ## Executive Summary
    Brief overview of code quality, major findings, and overall assessment.

    ## Critical Issues
    ### Bugs (Priority: Critical/High/Medium/Low)
    - `filename:line` - Description of bug and potential impact
    - Recommended fix or approach

    ### Security Vulnerabilities (Priority: Critical/High/Medium/Low)  
    - `filename:line` - Security issue description and risk level
    - Mitigation strategy

    ## Code Quality Analysis
    ### Performance Issues
    - `filename:line` - Performance concern and impact
    - Optimization suggestions

    ### Design and Architecture
    - Structural issues or improvements
    - Design pattern recommendations

    ### Style and Language Idioms
    - Consistency issues
    - Language-specific improvements
    - Formatting and convention adherence

    ## Positive Aspects
    - Well-implemented features or patterns
    - Good practices observed
    - Code strengths worth highlighting

    ## Recommendations
    ### Immediate Actions (Critical/High Priority)
    1. Most urgent fixes needed
    2. Security vulnerabilities to address

    ### Future Improvements (Medium/Low Priority)  
    1. Performance optimizations
    2. Code quality enhancements
    3. Architectural considerations

    ## Testing Recommendations
    - Areas requiring additional test coverage
    - Test improvement suggestions
    - Integration testing considerations

    ## Summary
    ### Overall Assessment
    - Code quality rating and justification
    - Readiness for production/deployment
    - Maintainability assessment

    ### Next Steps
    - Prioritized action items
    - Timeline recommendations
    ```
```