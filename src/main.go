// yaml2json
// Written by J.F. Gratton <jean-francois@famillegratton.net>
// Original timestamp: 2025/06/21 17:37
// Original filename: src/main.go

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"

	"gopkg.in/yaml.v3"
)

var version = fmt.Sprintf("1.1.2 2025.08.14 (ARCH=%s)", runtime.GOARCH)

func main() {
	// Handle 'changelog' command early
	if len(os.Args) > 1 && os.Args[1] == "changelog" {
		printChangelog()
		return
	}

	// Pre-parse to check for --version or -v without interfering with flag.Parse
	for _, arg := range os.Args[1:] {
		if arg == "--version" || arg == "-v" {
			fmt.Println("yaml2json version", version)
			return
		}
	}

	// Define flags
	force := flag.Bool("f", false, "Force conversion even if YAML validation fails")
	flag.Parse()

	args := flag.Args()
	if len(args) < 1 {
		fmt.Fprintf(os.Stderr, "Usage: %s [-f] <input.yaml> [output.json]\n", os.Args[0])
		os.Exit(1)
	}

	// Input/output file handling
	inFile := normalizeInputFile(args[0])
	var outFile string
	if len(args) >= 2 {
		outFile = args[1]
	} else {
		outFile = defaultOutFile(inFile)
	}

	// Read YAML file
	yamlData, err := os.ReadFile(inFile)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading input file: %v\n", err)
		os.Exit(1)
	}

	// Parse YAML
	var parsedData interface{}
	err = yaml.Unmarshal(yamlData, &parsedData)
	if err != nil {
		if *force {
			fmt.Fprintf(os.Stderr, "Warning: YAML parse error ignored due to -f flag: %v\n", err)
			var node yaml.Node
			if err := yaml.Unmarshal(yamlData, &node); err != nil {
				fmt.Fprintf(os.Stderr, "Failed to parse YAML even with -f: %v\n", err)
				os.Exit(1)
			}
			parsedData = yamlToMap(&node)
		} else {
			fmt.Fprintf(os.Stderr, "Invalid YAML: %v\n", err)
			os.Exit(1)
		}
	}

	// Convert to JSON
	jsonData, err := json.MarshalIndent(parsedData, "", "  ")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error converting to JSON: %v\n", err)
		os.Exit(1)
	}

	// Validate JSON output
	var validate interface{}
	err = json.Unmarshal(jsonData, &validate)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Generated JSON is invalid: %v\n", err)
		os.Exit(1)
	}

	// Write output
	err = os.WriteFile(outFile, jsonData, 0644)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to write JSON output: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("JSON output written to %s\n", outFile)
}

func normalizeInputFile(path string) string {
	ext := strings.ToLower(filepath.Ext(path))
	if ext != ".yml" && ext != ".yaml" {
		path += ".yaml"
	}
	return path
}

func defaultOutFile(input string) string {
	base := strings.TrimSuffix(input, filepath.Ext(input))
	return base + ".json"
}

func yamlToMap(n *yaml.Node) interface{} {
	switch n.Kind {
	case yaml.MappingNode:
		result := make(map[string]interface{})
		for i := 0; i < len(n.Content)-1; i += 2 {
			key := yamlToMap(n.Content[i])
			value := yamlToMap(n.Content[i+1])
			keyStr := fmt.Sprintf("%v", key)
			if _, exists := result[keyStr]; !exists {
				result[keyStr] = value
			}
		}
		return result
	case yaml.SequenceNode:
		var result []interface{}
		for _, item := range n.Content {
			result = append(result, yamlToMap(item))
		}
		return result
	case yaml.ScalarNode:
		var v interface{}
		_ = n.Decode(&v)
		return v
	default:
		return nil
	}
}

func printChangelog() {
	fmt.Println("Changelog:")
	fmt.Println("v1.00.01 (2025.06.22) :")
	fmt.Println("  - Flags cleanup")
	fmt.Println("v1.00.00 (2025.06.21) :")
	fmt.Println("  - Initial release")
	fmt.Println("  - Supports .yaml/.yml input to .json output")
	fmt.Println("  - --version flag")
	fmt.Println("  - -f flag to force conversion")
	fmt.Println("  - changelog command")
}
