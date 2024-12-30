#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

class TextExtractor {
public:
    template <typename T>
    class InnerClass {
    public:
        InnerClass(T func) : func(func) {}
        T func;
        void operator()(std::string& text) {
            func(text);
        }
    };

    TextExtractor() = default;

    void addText(const std::string& text) {
        texts.push_back(text);
    }

    void printTexts() const {
        for (const auto& text : texts) {
            std::cout << text << std::endl;
        }
    }

    template <typename T>
    void processTexts(T func) {
        InnerClass<T> innerProcessor(func);
        for (auto& text : texts) {
            innerProcessor(text);
        }
    }

private:
    std::vector<std::string> texts;
};

int main() {
    TextExtractor extractor;
    extractor.addText("Text1");
    extractor.addText("Text2");
    extractor.addText("Text3");

    std::cout << "Original Texts:" << std::endl;
    extractor.printTexts();

    auto toUpperCase = [](std::string& text) {
        std::transform(text.begin(), text.end(), text.begin(), ::toupper);
    };

    extractor.processTexts(toUpperCase);

    std::cout << "Processed Texts:" << std::endl;
    extractor.printTexts();

    return 0;
}
