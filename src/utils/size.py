size_config = {
    "small": {
        "16:9": {"height": 288, "width": 512},
        "3:2": {"height": 340, "width": 512},
        "4:3": {"height": 384, "width": 512},
        "5:4": {"height": 408, "width": 512},
        "1:1": {"height": 512, "width": 512},
        "4:5": {"height": 512, "width": 408},
        "3:4": {"height": 512, "width": 384},
        "2:3": {"height": 512, "width": 340},
        "9:16": {"height": 512, "width": 288}
    },
    "medium": {
        "16:9": {"height": 432, "width": 768},
        "3:2": {"height": 512, "width": 768},
        "4:3": {"height": 576, "width": 768},
        "5:4": {"height": 616, "width": 768},
        "1:1": {"height": 768, "width": 768},
        "3:4": {"height": 768, "width": 576},
        "4:5": {"height": 768, "width": 616},
        "2:3": {"height": 768, "width": 512},
        "9:16": {"height": 768, "width": 432}
    },
    "large": {
        "9:16": {"height": 1024, "width": 576},
        "3:2": {"height": 680, "width": 1024},
        "5:4": {"height": 820, "width": 1024},
        "3:4": {"height": 1024, "width": 768},
        "1:1": {"height": 1024, "width": 1024},
        "4:3": {"height": 768, "width": 1024},
        "4:5": {"height": 1024, "width": 820},
        "2:3": {"height": 1024, "width": 680},
        "16:9": {"height": 576, "width": 1024}
    }
}

sizes = {"small": 256, "medium": 512, "large": 768}

size_config_alt = {
    "3:2": {
        "small": {"height": 340, "width": 512},
        "medium": {"height": 512, "width": 768},
        "large": {"height": 680, "width": 1024}
    },
    "5:4": {
        "small": {"height": 408, "width": 512},
        "medium": {"height": 616, "width": 768},
        "large": {"height": 820, "width": 1024}
    },
    "1:1": {
        "small": {"height": 512, "width": 512},
        "medium": {"height": 768, "width": 768},
        "large": {"height": 1024, "width": 1024}
    },
    "4:5": {
        "small": {"height": 512, "width": 408},
        "medium": {"height": 768, "width": 616},
        "large": {"height": 1024, "width": 820}
    },
    "2:3": {
        "small": {"height": 512, "width": 340},
        "medium": {"height": 768, "width": 512},
        "large": {"height": 1024, "width": 680}
    }
}
