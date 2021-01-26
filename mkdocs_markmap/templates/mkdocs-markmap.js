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

        // todo: this is a dirty workaround to center the mindmap within svg
        (function(obj, e, r) {
            obj.rescale(1).then(function() {
                e.parentElement.style.height = (e.getBBox().height + 10) + "px";
                setTimeout(function() {
                    while (e.firstChild) {
                        e.removeChild(e.lastChild);
                    }
                    markmap.Markmap.create(e, null, r);
                }, 500);
            });
        })(m, svg, root);
    }
})();
