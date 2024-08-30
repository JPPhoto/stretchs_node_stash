from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    invocation,
    invocation_output,
)
from invokeai.app.invocations.fields import InputField, OutputField
from invokeai.app.services.shared.invocation_context import InvocationContext
import os
from typing import Union


@invocation_output("string_collection_joiner_output")
class StringCollectionJoinerOutput(BaseInvocationOutput):
    """String Collection Joiner Output"""

    result: str = OutputField(description="The joined string", title="Result")


@invocation("string_collection_joiner_invocation", title="String Collection Joiner", tags=["string"], category="string", version="1.0.0")
class StringCollectionJoinerInvocation(BaseInvocation):
    """Takes a collection of strings and returns a single string with all the collections items, separated by the input delimiter."""

    delimiter: str = InputField(title="Delimiter", description="The character to place between each string.", default=", ")
    collection: list[str] = InputField(title="Collection", description="The string collection to join.")

    def invoke(self, context: InvocationContext) -> StringCollectionJoinerOutput:
        return StringCollectionJoinerOutput(result=self.delimiter.join(self.collection))


@invocation_output("load_text_file_to_string_output")
class LoadTextFileToStringOutput(BaseInvocationOutput):
    """Load Text File To String Output"""

    result: str = OutputField(title="Result")


@invocation("load_text_file_to_string_invocation", title="Load Text File to String", tags=["string"], category="string", version="1.0.0", use_cache=False)
class LoadTextFileToStringInvocation(BaseInvocation):
    """Loads a text from a provided path and outputs it as a string"""

    file_path: str = InputField(title="Path", description="The full path to the text file.")

    def invoke(self, context: InvocationContext) -> LoadTextFileToStringOutput:
        with open(self.file_path, 'r') as file:
            # Read the entire file content into a string
            file_content = file.read()
        return LoadTextFileToStringOutput(result=file_content)



@invocation_output("load_all_text_files_in_folder_output")
class LoadAllTextFilesInFolderOutput(BaseInvocationOutput):
    """Load Text Files In Folder Output"""

    result: list[str] = OutputField(title="Results")


@invocation("load_all_text_files_in_folder_output", title="Load All Text Files In Folder", tags=["string"], category="string", version="1.0.1", use_cache=False)
class LoadAllTextFilesInFolderInvocation(BaseInvocation):
    """Loads all text files in a folder and returns them as a Collection of strings"""

    extension_to_match: str = InputField(title="File Extension", description="Only files with the given extension will be loaded. For example: json")
    folder_path: str = InputField(title="Folder Path", description="The path to load files from.")

    def invoke(self, context: InvocationContext) -> LoadAllTextFilesInFolderOutput:
        files_content = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith(self.extension_to_match):
                file_path = os.path.join(self.folder_path, filename)
                with open(file_path, 'r') as file:
                    files_content.append(file.read())
    
        return LoadAllTextFilesInFolderOutput(result=files_content)


@invocation_output("merge_string_collections_output")
class MergeStringCollectionsOutput(BaseInvocationOutput):
    """Merge String Collections output"""

    collection: list[str] = OutputField(description="The merged collection", title="Collection")


@invocation("merge_string_collections_invocation", title="Merge String Collections", tags=["collection", "string"], category="collection", version="1.0.0")
class MergeStringCollectionsInvocation(BaseInvocation):
    """Merges two Collections of LoRAs into a single Collection."""

    collection1: Union[str, list[str]] = InputField(title="Collection 1", description="A collection of strings or a single string.")
    collection2: Union[str, list[str]] = InputField(title="Collection 2", description="A collection of strings or a single string.")

    def invoke(self, context: InvocationContext) -> MergeStringCollectionsOutput:
        new_collection: list[str] = []
        new_collection.extend(self.collection1 if self.collection1 == list[str] else list[str](self.collection1))
        new_collection.extend(self.collection2 if self.collection2 == list[str] else list[str](self.collection2))
        return MergeStringCollectionsOutput(collection=new_collection)