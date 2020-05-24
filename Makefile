USER=praashie
REPO=flatmate
CURRENT_TAG=$(shell git describe --abbrev=0)

SOURCES=flatmate FLatmateExamples LICENSE
ARTIFACTS=dist

TARGET_ZIP=$(ARTIFACTS)/flatmate-$(CURRENT_TAG).zip

RELEASE_FLAGS=--user $(USER) --repo $(REPO) --tag $(CURRENT_TAG)

release: $(TARGET_ZIP)
	git push --tags
	github-release release $(RELEASE_FLAGS)
	github-release upload $(RELEASE_FLAGS) --file $(TARGET_ZIP)

$(TARGET_ZIP): $(SOURCES)
	mkdir -p $(ARTIFACTS)
	git clean -Xf
	zip -r $@ $(SOURCES)

clean:
	rm -rf $(ARTIFACTS)
