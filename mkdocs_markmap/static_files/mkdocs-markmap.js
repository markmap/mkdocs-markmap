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
        options = Object.assign({
            fitRatio: 0.85,
        }, options);
        return { root, options };
    }

    function resetMarkmap(m, el) {
        const { minX, maxX, minY, maxY } = m.state;
        const height = el.clientWidth * (maxX - minX) / (maxY - minY);
        el.style.height = height + "px";
        m.fit();
    }

    function renderMarkmap(el) {
        let svg = el.querySelector('svg');
        if (svg) return;
        const content = el.textContent;
        el.innerHTML = '<svg>';
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

    function updateMarkmaps() {
        const markmaps = document.getElementsByClassName('mkdocs-markmap');
        for (var i = 0; i < markmaps.length; i++) {
            const el = markmaps[i];
            renderMarkmap(el);
        }
    }

    loading.then(() => {
        var MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
        var observer = new MutationObserver(function(mutations) {
            updateMarkmaps();
        });

        var target = document.getElementById('mkdocs-decrypted-content');
        if (undefined != target) {
            observer.observe(target, { childList: true });
        }

        updateMarkmaps();
    });
})();
