from marshmallow import Schema, fields, INCLUDE, validate


class IdentifierSchema(Schema):

    system = fields.URL(required=True)
    value = fields.String(required=True)


class ClassSchema(Schema):

    system = fields.URL(required=True)
    code = fields.String(required=True)


class CodingSchema(Schema):

    coding = fields.List(fields.Nested(ClassSchema, required=True))


class SubjectSchema(Schema):

    reference = fields.String(required=True)


class PeriodSchema(Schema):

    start = fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True)


class ResourceTypeSchema(Schema):
    class Meta:
        unknown = INCLUDE

    resourceType = fields.String(validate=validate.OneOf(["Encounter", "Patient", "Consent"]), required=True)
    id = fields.UUID()
    identifier = fields.List(fields.Nested(IdentifierSchema))
    status = fields.String(validate=validate.OneOf(["planned", "arrived", "triaged", "in-progress", "onleave",
                                                    "finished", "cancelled"]))
    cls = fields.Nested(ClassSchema, data_key="class")
    type = fields.List(fields.Nested(CodingSchema))
    subject = fields.Nested(SubjectSchema)
    period = fields.Nested(PeriodSchema)


class ResourceSchema(Schema):

    resource = fields.Nested(ResourceTypeSchema, required=True)


class IntakeApiSchema(Schema):

    resourceType = fields.String(required=True)
    type = fields.String(required=True)
    entry = fields.List(fields.Nested(ResourceSchema), required=True)
