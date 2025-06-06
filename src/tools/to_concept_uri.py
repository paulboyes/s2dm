import json
import logging
from pathlib import Path

import click

from concept.services import create_concept_uri_model, iter_all_concepts
from tools.utils import get_all_named_types, load_schema

logger = logging.getLogger(__name__)


@click.command()
@click.argument("schema", type=click.Path(exists=True), required=True)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    help="Output file path for the JSON-LD file",
)
@click.option(
    "--namespace",
    default="https://example.org/vss#",
    help="The namespace for the URIs",
)
@click.option(
    "--prefix",
    default="ns",
    help="The prefix to use for the URIs",
)
def main(
    schema: Path,
    output: Path | None,
    namespace: str,
    prefix: str,
):
    """Generate concept URIs for a GraphQL schema.

    The script will generate concept URIs for all objects, fields, and enums in the schema,
    excluding cross-references and ID fields. The URIs will be output in JSON-LD format.
    """
    logging.info(f"Processing schema '{schema}'")

    # Load the schema
    graphql_schema = load_schema(schema)

    # Process the schema to get concepts
    concepts = iter_all_concepts(get_all_named_types(graphql_schema))

    # Create concept URI model
    concept_uri_model = create_concept_uri_model(concepts, namespace, prefix)

    # Output options
    if output:
        with open(output, "w", encoding="utf-8") as output_file:
            logger.info(f"Writing data to '{output}'")
            json.dump(concept_uri_model.to_json_ld(), output_file, indent=2)
    else:
        print("-" * 80)
        print(json.dumps(concept_uri_model.to_json_ld(), indent=2))


if __name__ == "__main__":
    main()
