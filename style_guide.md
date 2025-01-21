# Style Guide

## Framework

Follow the [Diátaxis approach](https://diataxis.fr/) when you think about and work on new documentation. 
This approach helps you decide on what kind of documentation to write and how to write it well. 

## Voice

Documents should be written mainly in a combination of "second person" and "active voice", depending on the context.

### Second Person

Address the reader directly, often using "you".
For example, "You need to create a HTTPRoute",
rather than saying "An HTTPRoute needs to be created by you."

### Active Voice

The subject of the sentence performs the action.
For example, "The Gateway controller processes the HTTPRoute to establish routing rules",
rather than saying "The HTTPRoute is processed by the Gateway controller to establish routing rules"

## Tense

Use present tense, unless the meaning is better conveyed in future or past tense.
For example, "This command starts the operator"
rather than "This command will start the operator"

## Language

Use simple and direct language. Avoid unnecessary phrases, such as saying 'please'.
For example, use "To create a ReplicaSet,..." instead of "In order to create a ReplicaSet, ...".
Another example, use "View the pods." instead of "With this next command, we'll view the pods".

## Avoid jargon and idioms

Some readers may not speak English as a primary language. Avoid jargon and idioms to help them understand better.
For example, use "Internally,..." instead of "Under the hood,...",
or "Create a new cluster." instead of "Spin up a cluster."

## Avoid time sensitive statements

Avoid making promises or giving hints about the future. If you need to talk about an alpha feature, put the text under a heading that identifies it as alpha information.
An exception to this would be mentioning the deprecation (and potential eventual removal) of some API.

Avoid statements that will soon be out of date.
An indication of this is words like "currently" and "new." A feature that is new today might not be considered new in a few months.

For example, use "In version 1.0, ..." instead of "In the current version, ...".

## Avoid words that don't add value

Avoid words such as "just", "simply", "easy", "easily", or "simple". These words do not add value.

## Images

Avoid the overuse of images and screenshots as they can be a pain to maintain.

## Characters

Avoid the use of unusual characters, for example Unicode numbering and emojis.

## Grammar

* Start sentences with capital letters and end with . or :
* Products, projects, and tools should be capitalised i.e Kuadrant, Authorino, Limitador etc

## Inline Blocks, Notes & Warnings

To highlight some content like blocks, notes or warnings, use the correct formatting as per https://squidfunk.github.io/mkdocs-material/reference/admonitions/#inline-blocks

For example:

````markdown
```markdown
!!! note

    This method currently only works if the Gateway is provided by Istio, with service mesh capabilities enabled across the cluster.
```
````

## Code Blocks

For code blocks preface the language in the code block as per https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#usage

For example:

````markdown
```bash
kubectl get deployments -n kuadrant-system
```
````

## Numbering in lists

Avoid the overuse of numbering. It allows for docs to be updated much easier in the future.

## Environment Variables

Environment variables should be capitalised and use 'KUADRANT_' at the start, for example, `KUADRANT_GATEWAY_NS`, unless they are already defined environment variables for existing tools and services.
