

# ADD

def add_triangulate(obj):
    mod = obj.modifiers.new(name="Triangulate", type="TRIANGULATE")
    mod.keep_custom_normals = True
    mod.quad_method = 'FIXED'
    mod.show_expanded = True
    return mod


def add_shrinkwrap(obj, target):
    mod = obj.modifiers.new(name="Shrinkwrap", type="SHRINKWRAP")

    mod.target = target
    mod.show_on_cage = True
    mod.show_expanded = False
    return mod


# REMOVE

def remove_triangulate(obj):
    lastmod = obj.modifiers[-1] if obj.modifiers else None

    if lastmod and lastmod.type == 'TRIANGULATE':
        obj.modifiers.remove(lastmod)
        return True
