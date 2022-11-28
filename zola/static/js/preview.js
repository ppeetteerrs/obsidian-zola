const cache = new Map();

function showPreview(mouseEvent, link) {
    const { clientX, clientY } = mouseEvent;
    let previewDiv = createPreview();

    previewDiv.innerHTML = "Loading... ⏳";

    const html = cache.get(link.href);
    if (!html) {
        fetch(`${link.href}`)
            .then((res) => res.text())
            .then((html) => {
                let doc = new DOMParser().parseFromString(html, "text/html");
                let docContent = doc.querySelector(".docs-content");
                previewDiv.innerHTML = docContent.innerHTML;

                let blockId = link.href.match(/(?<=#).{6}/);

                if (blockId != null) {
                    blockId = [blockId];
                    const blockContent = [
                        ...docContent.querySelectorAll(
                            "p, li, h1, h2, h3, h4, h5, h6"
                        ),
                    ].findLast((e) => {
                        return e.textContent.includes(`^${blockId}`);
                    });

                    previewDiv.innerHTML = blockContent.outerHTML;
                }
                cache.set(link.href, previewDiv.innerHTML);
                previewDiv.addEventListener("dragstart", (e) => {
                    e.preventDefault();
                    console.log(e.offsetX, e.offsetY);
                }, false);
                initPreview(`.${getPreviewUniqueClass(previewDiv)} a`);
            });
    } else {
        previewDiv.innerHTML = html;
        initPreview(`.${getPreviewUniqueClass(previewDiv)} a`);
    }

    const { top, right } = getPreviewPosition(clientX, clientY);
    previewDiv.style.top = `${top}px`;
    previewDiv.style.right = `${right}px`;

    previewDiv.addEventListener("mouseleave", () => {
        handleMouseLeave();
    });

    link.addEventListener(
        "mouseleave",
        () => {
            setTimeout(() => {
                if (!previewDiv.matches(":hover")) {
                    hidePreview(previewDiv);
                }
            }, 200);
        },
        false
    );
}

function getPreviewPosition(clientX, clientY) {
    const offset = 10,
        previewDivWidth = 400,
        previewDivHeight = 100;
    const boundaryX = window.innerWidth,
        boundaryY = window.innerHeight;
    const overflowRight = clientX + offset + previewDivWidth > boundaryX;
    const overflowLeft = clientX - offset - previewDivWidth < 0;
    const overflowBottom = clientY + offset + previewDivHeight > boundaryY;
    const position = { top: offset, right: offset };

    if (!overflowRight) {
        position.right = boundaryX - clientX - offset - previewDivWidth;
    } else if (!overflowLeft) {
        position.right = boundaryX - clientX - offset;
    }

    if (!overflowBottom) {
        position.top = clientY + offset;
    } else {
        position.top = clientY - offset - previewDivHeight;
    }

    return position;
}

function handleMouseLeave() {
    setTimeout(() => {
        const allPreviews = document.querySelectorAll(".preview");
        for (let i = allPreviews.length - 1; i >= 0; i--) {
            const curr = allPreviews[i];
            if (curr.matches(":hover")) {
                break;
            }
            hidePreview(curr);
        }
    }, 300);
}

function getPreviewUniqueClass(previewDiv) {
    return previewDiv.classList.item(previewDiv.classList.length - 1);
}

function isDocLink(href) {
    const test = new URL(href);
    return test.pathname.startsWith("/docs/");
}

function hidePreview(previewDiv) {
    try {
        document.body.removeChild(previewDiv);
    } catch (e) {}
}

function createPreview() {
    const previewDiv = document.createElement("div");
    const uniqueClassName = (Math.random() + 1).toString(36).substring(7);
    previewDiv.classList.add("preview");
    previewDiv.classList.add(`preview_${uniqueClassName}`);
    document.querySelector("body").appendChild(previewDiv);
    return previewDiv;
}

function initPreview(query = ".docs-content a") {
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) return;

    document.querySelectorAll(query).forEach((a) => {
        if (isDocLink(a.href)) {
            a.addEventListener("mouseover", (e) => showPreview(e, a), false);
        }
    });
}

initPreview();
