if (
    "IntersectionObserver" in window &&
    "IntersectionObserverEntry" in window &&
    "intersectionRatio" in window.IntersectionObserverEntry.prototype
    ) {
        let observer = new IntersectionObserver(entries => {
            if (entries[0].boundingClientRect.y < 0) {
                document.querySelector("#scrollToTopBtn").classList.remove("hidden");
            } else {
                document.querySelector("#scrollToTopBtn").classList.add("hidden");
            }
        });
        observer.observe(document.querySelector("#top-of-site-pixel-anchor"));
    }