(function initializeMarkmap() {
    const markmap_transformer = new markmap.Transformer();
    const markmaps = document.getElementsByClassName('mkdocs-markmap');
    var el, content, svg, root, m;
    for (var i = 0; i < markmaps.length; i++) {
        el = markmaps[i];
        content = el.getAttribute('data-markdown').replaceAll('&#10;', '\n');
        svg = el.querySelector('svg');
        root = markmap_transformer.transform(content).root;
        m = markmap.Markmap.create(svg, null, root);

        (function(obj, e, r) {
            obj.rescale(1).then(function() {
                e.parentElement.style.height = (e.getBBox().height + 10) + "px";
                requestAnimationFrame(() => { obj.fit(); })
            });
        })(m, svg, root);
    }
})();
