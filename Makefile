USER=praashie
REPO=flatmate
CURRENT_TAG=$(shell git describe --abbrev=0)

SOURCES=flatmate FLatmateExamples LICENSE
ARTIFACTS=dist

ZIP_NAME=flatmate-$(CURRENT_TAG).zip
TARGET_ZIP=$(ARTIFACTS)/$(ZIP_NAME)

RELEASE_FLAGS=--user $(USER) --repo $(REPO) --tag $(CURRENT_TAG)

release: $(TARGET_ZIP)
	git push --tags
	github-release release $(RELEASE_FLAGS)
	github-release upload $(RELEASE_FLAGS) --file $(TARGET_ZIP) --name $(ZIP_NAME)

$(TARGET_ZIP): $(SOURCES)
	mkdir -p $(ARTIFACTS)
	git clean -Xf
	zip -r $@ $(SOURCES)

clean:
	rm -rf $(ARTIFACTS)
