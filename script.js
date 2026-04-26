"use strict";

/**
 * @param {string} id 
 * @returns {void}
 */
function openDialog(id) {
    const imgEl = document.getElementById('dialog-img');
    if (!imgEl) {
        return;
    }
    imgEl.setAttribute('data-flag', id);
    imgEl.setAttribute('src', id + '.svg');

    const dialogEl = /** @type {HTMLDialogElement?} */ (document.getElementById('dialog'));
    dialogEl?.showModal();
}

function init() {
    const flags = (document.body.getAttribute('data-flags') ?? '').split(/\s+/);

    /** @type {Map<string, number>} */
    const flagMap = new Map();
    for (let index = 0; index < flags.length; ++ index) {
        flagMap.set(flags[index], index);
    }

    const prevEl = document.getElementById('dialog-prev');
    const nextEl = document.getElementById('dialog-next');

    prevEl?.addEventListener('click', event => {
        const imgEl = document.getElementById('dialog-img');
        if (!imgEl) {
            return;
        }

        const flag = imgEl.getAttribute('data-flag');
        if (!flag) {
            return;
        }

        const index = flagMap.get(flag);
        if (index === undefined) {
            return;
        }

        const newFlag = index === 0 ? flags[flags.length - 1] : flags[index - 1];

        imgEl.setAttribute('data-flag', newFlag);
        imgEl.setAttribute('src', newFlag + '.svg');
    });

    nextEl?.addEventListener('click', event => {
        const imgEl = document.getElementById('dialog-img');
        if (!imgEl) {
            return;
        }

        const flag = imgEl.getAttribute('data-flag');
        if (!flag) {
            return;
        }

        const index = flagMap.get(flag);
        if (index === undefined) {
            return;
        }

        const newFlag = flags[(index + 1) % flags.length];

        imgEl.setAttribute('data-flag', newFlag);
        imgEl.setAttribute('src', newFlag + '.svg');
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
