#include "emscripten.h"
#include "hack.h"
#include <malloc.h>
#include <string.h>
#include <stdint.h>

EMSCRIPTEN_KEEPALIVE
const char* version() {
    return cmark_version_string();
}

typedef struct ExtensionList {
    cmark_llist* extensions;
    cmark_llist* cur;
    cmark_mem* mem;
} ExtensionList;

EMSCRIPTEN_KEEPALIVE
ExtensionList* new_extension_list() {
    ExtensionList* e = malloc(sizeof(ExtensionList));
    if (!e) return NULL;
    e->extensions = NULL;
    e->cur = NULL;
    e->mem = cmark_get_default_mem_allocator();
    return e;
}

EMSCRIPTEN_KEEPALIVE
int append_extension_to_list(ExtensionList* e, const char* name) {
    if (!e || !name) return 1;
    cmark_gfm_core_extensions_ensure_registered();
    cmark_syntax_extension* ext = cmark_find_syntax_extension(name);
    if (!ext) return 1;
    e->extensions = cmark_llist_append(e->mem, e->extensions, (void*)ext);
    return 0;
}

EMSCRIPTEN_KEEPALIVE
ExtensionList* get_all_extensions() {
    cmark_gfm_core_extensions_ensure_registered();
    cmark_mem* mem = cmark_get_default_mem_allocator();
    ExtensionList* e = malloc(sizeof(ExtensionList));
    if (!e) {
        return NULL;
    }
    e->extensions = NULL;
    e->cur = NULL;
    e->mem = mem;
    e->extensions = cmark_list_syntax_extensions(mem);
    if (!e->extensions) {
        free(e);
        return NULL;
    }
    e->cur = e->extensions;
    return e;
}

EMSCRIPTEN_KEEPALIVE
char* get_next_extension_name(ExtensionList* list, int32_t* le) {
    if (!list->cur) {
        if (le) *le = 0;
        return NULL;
    }
    cmark_syntax_extension* ext = (cmark_syntax_extension*) list->cur->data;
    list->cur = list->cur->next;
    size_t l = strlen(ext->name);
    char* n = malloc(l + 1);
    if (!n) {
        if (le) *le = 0;
        return NULL;
    }
    memcpy(n, ext->name, l);
    n[l] = 0;
    if (le) *le = l;
    return n;
}

EMSCRIPTEN_KEEPALIVE
void free_extension_list(ExtensionList* e) {
    if (!e) return;
    if (e->extensions) {
        cmark_llist_free(e->mem, e->extensions);
        e->extensions = NULL;
    }
    free(e);
}

EMSCRIPTEN_KEEPALIVE
char* md_to_html(const char* text, size_t len, int options, ExtensionList* ext) {
    cmark_parser* p = cmark_parser_new(options);
    if (!p) return NULL;
    char* result = NULL;
    cmark_node* doc = NULL;
    if (ext && ext->extensions) {
        cmark_llist* tmp = ext->extensions;
        for (; tmp; tmp = tmp->next) {
            if (!cmark_parser_attach_syntax_extension(p, (cmark_syntax_extension*)tmp->data)) goto end;
        }
    }
    cmark_parser_feed(p, text, len);
    doc = cmark_parser_finish(p);
    if (!doc) goto end;
    cmark_llist* exts = NULL;
    if (ext && ext->extensions) exts = ext->extensions;
    result = cmark_render_html(doc, options, exts);
end:
    if (doc) cmark_node_free(doc);
    if (p) cmark_parser_free(p);
    return result;
}
