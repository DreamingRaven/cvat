# Copyright (C) 2021-2022 Intel Corporation
#
# SPDX-License-Identifier: MIT

import coreapi
from rest_framework.filters import BaseFilterBackend

class OrganizationFilterBackend(BaseFilterBackend):
    organization_slug = 'org'
    organization_slug_description = 'Organization unique slug'
    organization_id = 'org_id'
    organization_id_description = 'Organization identifier'

    def get_schema_fields(self, view):
        return [
            # NOTE: in coreapi.Field 'type', 'description' and 'example' are now deprecated, in favor of 'schema'.
            coreapi.Field(name=self.organization_slug, location='query', required=False,
                type='string', description=self.organization_slug_description),
            coreapi.Field(name=self.organization_id, location='query', required=False,
                type='string', description=self.organization_id_description),
        ]

    def filter_queryset(self, request, queryset, view):
        # Rego rules should filter objects correctly (see filter rule). The
        # filter isn't necessary but it is an extra check that we show only
        # objects inside an organization if the request in context of the
        # organization.

        if view.action != "list":
            return queryset

        visibility = None
        org = request.iam_context["organization"]

        if org:
            visibility = {'organization': org.id}

        elif not org and ('org' in request.query_params or 'org_id' in request.query_params):
            visibility = {'organization': None}

        if visibility and view.iam_organization_field:
            visibility[view.iam_organization_field] = visibility.pop('organization')
            return queryset.filter(**visibility).distinct()

        return queryset
