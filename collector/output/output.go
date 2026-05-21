package output

import (
	"encoding/json"
	"os"
	"path/filepath"

	"collector/model"
)

func WriteJSON(path string, data model.NewsOutput) error {
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		return err
	}

	f, err := os.Create(path)
	if err != nil {
		return err
	}
	defer f.Close()

	enc := json.NewEncoder(f)
	enc.SetIndent("", "  ")
	return enc.Encode(data)
}
