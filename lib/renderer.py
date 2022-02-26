from json_schema_for_humans.generation_configuration import GenerationConfiguration
from json_schema_for_humans.schema.intermediate_representation import (
    build_intermediate_representation,
)
from json_schema_for_humans.template_renderer import TemplateRenderer


def get_config(query_params):
    return GenerationConfiguration(
        minify=False,
        description_is_markdown=bool(query_params.get("description_is_markdown")),
        deprecated_from_description=bool(
            query_params.get("deprecated_from_description")
        ),
        show_breadcrumbs=bool(query_params.get("show_breadcrumbs")),
        collapse_long_descriptions=bool(query_params.get("collapse_long_descriptions")),
        default_from_description=bool(query_params.get("default_from_description")),
        expand_buttons=bool(query_params.get("expand_buttons")),
        copy_css=False,
        copy_js=False,
        link_to_reused_ref=True,
        recursive_detection_depth=25,
        template_name=query_params.get("template_name", "js"),
        custom_template_path=None,
        show_toc=bool(query_params.get("show_toc")),
        examples_as_yaml=bool(query_params.get("examples_as_yaml")),
        with_footer=bool(query_params.get("with_footer")),
        footer_show_time=False,
    )


def render_schema(schema, config):
    template_renderer = TemplateRenderer(config)

    with open(schema) as f:
        intermediate_schema = build_intermediate_representation(f, config)

    return template_renderer.render(intermediate_schema)
