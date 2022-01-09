from json_schema_for_humans.generation_configuration import GenerationConfiguration
from json_schema_for_humans.schema.intermediate_representation import (
    build_intermediate_representation,
)
from json_schema_for_humans.template_renderer import TemplateRenderer


def render_schema(schema):
    config = GenerationConfiguration(
        minify=False,
        description_is_markdown=True,
        deprecated_from_description=False,
        show_breadcrumbs=True,
        collapse_long_descriptions=False,
        default_from_description=False,
        expand_buttons=True,
        copy_css=False,
        copy_js=False,
        link_to_reused_ref=True,
        recursive_detection_depth=25,
        template_name="js",
        custom_template_path=None,
        show_toc=False,
        examples_as_yaml=False,
        with_footer=True,
        footer_show_time=False,
    )

    template_renderer = TemplateRenderer(config)

    with open(schema) as f:
        intermediate_schema = build_intermediate_representation(f, config)

    return template_renderer.render(intermediate_schema)
