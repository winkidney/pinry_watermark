# pinry_watermark
watermark example plugin for pinry


Just run `pip install -e .` in pinry's same python interpreter and then add config to django settings:

```
ENABLED_PLUGINS = [
    'pinry_watermark.Plugin',
]
```

The watermark plugin will works like a charm.
