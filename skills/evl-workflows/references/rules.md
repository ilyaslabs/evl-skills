<!-- Generated from ilyaslabs/evl-lib spec at b715bc0b9f22 by tools/generate_references.py. Do not edit. -->

# EVL validation rules

Every diagnostic `evl validate` can report. `configurable: no` means the level cannot be changed in `evl.yaml` `rules:`.

| Code | Level | Title | Meaning | Configurable |
|---|---|---|---|---|
| `EVL-E001` | ERROR | Invalid manifest | evl.yaml is missing required fields (evl, id, name) or has invalid values. | no |
| `EVL-E002` | ERROR | Overlapping manifests | More than one evl.yaml claims the same source root. | no |
| `EVL-E010` | ERROR | Duplicate id | Two declarations use the same id (an annotation plus a YAML element with the same id merge instead). | yes |
| `EVL-E011` | ERROR | Malformed id | Ids are dotted lowercase segments: [a-z][a-z0-9-]* separated by dots, at most 128 characters. | yes |
| `EVL-E012` | ERROR | Missing id | Elements declared in documents must have an id. | yes |
| `EVL-E020` | ERROR | Conflicting source | An annotation and a YAML element with the same id point at different source locations. | yes |
| `EVL-E021` | ERROR | Reference kind mismatch | The kind prefix of a reference does not match the target element's kind. | yes |
| `EVL-E022` | ERROR | Library not found | A reference names an EVL library (app-id:) that is not on the classpath. | yes |
| `EVL-E023` | ERROR | Wrong reference target | The attribute does not allow references to elements of this kind. | yes |
| `EVL-E024` | ERROR | Library element override | A consuming application cannot redeclare an element of a library. | yes |
| `EVL-E025` | ERROR | Unresolved reference | The referenced element does not exist. | yes |
| `EVL-E030` | ERROR | Unresolved source reference | The source reference does not resolve to code. | yes |
| `EVL-E031` | ERROR | Ambiguous source reference | The source reference matches several members; add parameter types. | yes |
| `EVL-E032` | ERROR | Duplicate library | Two libraries with the same EVL id are on the classpath. | yes |
| `EVL-E033` | ERROR | Malformed source reference | The source reference does not follow the syntax type[#member[(params)]]. | yes |
| `EVL-E050` | ERROR | Major version mismatch | A document declares a different major spec version than the manifest. | yes |
| `EVL-E052` | ERROR | Unsupported spec version | The manifest declares a major spec version this tool does not support. | yes |
| `EVL-E060` | ERROR | Unknown step type | The step type is not one of the official step types. | yes |
| `EVL-E061` | ERROR | Duplicate step id | Step ids must be unique within their flow. | yes |
| `EVL-E062` | ERROR | Unknown goto target | A GOTO step targets a step id that does not exist in the same flow. | yes |
| `EVL-E063` | ERROR | Decision needs two branches | A DECISION step needs at least two branches (counting otherwise). | yes |
| `EVL-E064` | ERROR | Parallel needs two branches | A PARALLEL step needs at least two branches. | yes |
| `EVL-E065` | ERROR | Call target is not a flow | A CALL_FLOW step must reference a flow. | yes |
| `EVL-E066` | ERROR | Field not allowed for step type | The step declares a field that its type does not accept. | yes |
| `EVL-E067` | ERROR | Missing step field | The step type requires a field that is missing (e.g. flow for CALL_FLOW, target for GOTO). | yes |
| `EVL-E068` | ERROR | Unknown flow input | A CALL_FLOW input name is not declared by the called flow. | yes |
| `EVL-E070` | ERROR | Sensitive default value | A sensitive config property must not declare a default value. | yes |
| `EVL-E071` | ERROR | Possible secret | Text looks like a secret (private key, access key, password or high-entropy token). | yes |
| `EVL-E100` | ERROR | YAML tag not allowed | Custom YAML tags are not allowed in EVL documents. | no |
| `EVL-E101` | ERROR | Duplicate YAML key | A mapping declares the same key twice. | no |
| `EVL-E102` | ERROR | Unknown field | The field is not defined for this element kind (use an x- prefix for extensions). | no |
| `EVL-E103` | ERROR | Wrong value type | The value does not have the type the schema requires. | no |
| `EVL-E104` | ERROR | YAML syntax error | The document is not valid YAML. | no |
| `EVL-E105` | ERROR | Document too large | The document exceeds a size, depth or alias limit. | yes |
| `EVL-E106` | ERROR | Missing required field | A required field is missing. | yes |
| `EVL-E107` | ERROR | Invalid enum value | The value is not one of the allowed values. | yes |
| `EVL-W001` | WARNING | Missing manifest | No evl.yaml was found; an application id was derived. | yes |
| `EVL-W002` | WEAK_WARNING | Derived id | The annotation has no explicit id; the derived id changes when the class is renamed. | yes |
| `EVL-W021` | WARNING | Recursive flow | A flow calls itself directly or indirectly. | yes |
| `EVL-W051` | WARNING | Newer minor version | The document uses a newer minor spec version than this tool supports. | yes |
| `EVL-W060` | WEAK_WARNING | Step order from annotations | Steps declared only by @EVL.Step are ordered by source position, which is not guaranteed across files. | yes |
| `EVL-W061` | WEAK_WARNING | Default category | The flow has no category; APPLICATION is assumed. | yes |
| `EVL-W066` | WARNING | Unreachable steps | Steps after FAIL, END or an unconditional GOTO never run. | yes |
| `EVL-W067` | WARNING | Unconditional loop | A GOTO jumps backwards without a when condition. | yes |
| `EVL-W071` | WARNING | Orphan doc | @EVL.Doc is not attached to any EVL element. | yes |
| `EVL-W080` | WARNING | Outside module packages | The element's source is outside the packages of its module. | yes |
| `EVL-I020` | INFO | Overridden by YAML | Fields of an annotation are overridden by a YAML declaration. | yes |
| `EVL-I030` | INFO | Unrealized business step | A BUSINESS flow step has neither realizedBy nor source. | yes |
| `EVL-I040` | INFO | Dependency not seen in code | No code reference supports this declared dependency (it may be indirect). | yes |
| `EVL-I041` | INFO | Source not checked | The source reference could not be checked (no compiled classes or sources available). | yes |
