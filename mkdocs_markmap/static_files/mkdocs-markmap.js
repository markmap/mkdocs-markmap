(function initializeMarkmap() {
    const transformer = new markmap.Transformer();
    const assets = transformer.getAssets();
    const loading = Promise.all([
        assets.styles && markmap.loadCSS(assets.styles),
        assets.scripts && markmap.loadJS(assets.scripts),
    ]);

    function parseData(content) {
        const { root, frontmatter } = transformer.transform(content);
        let options = markmap.deriveOptions(frontmatter?.markmap);
        options = Object.assign(
            {
                fitRatio: 0.85,
            },
            options
        );
        return { root, options };
    }

    function resetMarkmap(m, el) {
        const { minX, maxX, minY, maxY } = m.state;
        const height = (el.clientWidth * (maxX - minX)) / (maxY - minY);
        el.style.height = height + "px";
        m.fit();
    }

    function decodeBase64(encoded) {
        const binary = atob(encoded);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < bytes.length; i++) {
            bytes[i] = binary.charCodeAt(i);
        }
        return new TextDecoder().decode(bytes);
    }

    function renderMarkmap(el) {
        const dataEl = el.querySelector("markmap-data");
        if (!dataEl) return;
        let content = el.textContent;
        if (dataEl.getAttribute("encoding") === "base64") {
            content = decodeBase64(content);
        }
        el.innerHTML = "<svg>";
        svg = el.firstChild;
        const { root, options } = parseData(content);
        const m = markmap.Markmap.create(svg, options, root);
        resetMarkmap(m, el);
        transformer.hooks.retransform.tap(() => {
            const { root, options } = parseData(content);
            m.setData(root, options);
            resetMarkmap(m, el);
        });
    }

    function updateMarkmaps(node) {
        for (const el of node.querySelectorAll(".mkdocs-markmap")) {
            renderMarkmap(el);
        }
    }

    loading.then(() => {
        const observer = new MutationObserver((mutationList) => {
            for (const mutation of mutationList) {
                if (mutation.type === "childList") {
                    for (const node of mutation.addedNodes) {
                        updateMarkmaps(node);
                    }
                }
            }
        });

        observer.observe(document.body, { childList: true });

        updateMarkmaps(document);
    });
})();
