from marshmallow import Schema, fields, INCLUDE, validate


class IdentifierSchema(Schema):

    system = fields.URL(required=True)
    value = fields.String(required=True)


class AuthorSiteSchema(Schema):

    author = fields.Nested(IdentifierSchema, required=True)
    site = fields.Nested(IdentifierSchema, required=True)


class SampleSchema(Schema):
    class Meta:
        unknown = INCLUDE

    test = fields.String(required=True)
    description = fields.String(required=True)
    collected = fields.String(required=True)
    finalized = fields.String(required=True)


class AliquotSchema(Schema):

    id = fields.String(required=True)
    identifier = fields.String(required=True)
    container = fields.String(required=True)
    volume = fields.String(required=True)
    description = fields.String(required=True)
    collected = fields.String(required=True)


class NotesSchema(Schema):

    collected = fields.String(required=True)
    finalized = fields.String(required=True)


class AmendedInfoSchema(Schema):

    author = fields.Nested(IdentifierSchema, required=True)
    site = fields.Nested(IdentifierSchema, required=True)


class OrderSchema(Schema):

    subject = fields.String(required=True)
    identifier = fields.List(fields.Nested(IdentifierSchema), required=True)
    createdInfo = fields.Nested(AuthorSiteSchema, required=True)
    collectedInfo = fields.Nested(AuthorSiteSchema, required=True)
    finalizedInfo = fields.Nested(AuthorSiteSchema, required=True)
    created = fields.String(required=True)
    module = fields.String(required=True)
    visitType = fields.String(required=True)
    timepoint = fields.String(required=True)
    sample = fields.Nested(SampleSchema, required=True)
    aliquots = fields.List(fields.Nested(AliquotSchema))
    notes = fields.Nested(NotesSchema, required=True)


class RestoredUpdateSchema(Schema):

    status = fields.String(validate=validate.OneOf(["cancelled", "restored", "CANCELLED", "RESTORED"]), required=True)
    amendedReason = fields.String(required=True)
    restoredInfo = fields.Nested(AmendedInfoSchema, required=True)


class CancelledUpdateSchema(Schema):

    status = fields.String(validate=validate.OneOf(["cancelled", "restored", "CANCELLED", "RESTORED"]), required=True)
    amendedReason = fields.String(required=True)
    cancelledInfo = fields.Nested(AmendedInfoSchema, required=True)

