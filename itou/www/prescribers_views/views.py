from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from itou.common_apps.organizations.views import deactivate_org_member, update_org_admin_role
from itou.prescribers.models import PrescriberOrganization
from itou.users.models import User
from itou.utils.perms.prescriber import get_current_org_or_404
from itou.utils.urls import get_safe_url
from itou.www.prescribers_views.forms import EditPrescriberOrganizationForm


def card(request, org_id, template_name="prescribers/card.html"):
    """
    Prescriber organization's card (or "Fiche" in French).
    """
    prescriber_org = get_object_or_404(PrescriberOrganization, pk=org_id, is_authorized=True)
    back_url = get_safe_url(request, "back_url")
    context = {"prescriber_org": prescriber_org, "back_url": back_url}
    return render(request, template_name, context)


@login_required
def edit_organization(request, template_name="prescribers/edit_organization.html"):
    """
    Edit a prescriber organization.
    """
    organization = get_current_org_or_404(request)
    if not organization.has_admin(request.user):
        raise PermissionDenied

    form = EditPrescriberOrganizationForm(instance=organization, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Mise à jour effectuée !")
        return HttpResponseRedirect(reverse_lazy("dashboard:index"))

    context = {"form": form, "organization": organization}
    return render(request, template_name, context)


@login_required
def member_list(request, template_name="prescribers/members.html"):
    """
    List members of a prescriber organization.
    """
    organization = get_current_org_or_404(request)

    members = (
        organization.prescribermembership_set.filter(is_active=True)
        .select_related("user")
        .all()
        .order_by("-is_admin", "joined_at")
    )
    pending_invitations = organization.invitations.pending()

    context = {
        "organization": organization,
        "members": members,
        "pending_invitations": pending_invitations,
    }
    return render(request, template_name, context)


@login_required
def deactivate_member(request, user_id, template_name="prescribers/deactivate_member.html"):
    organization = get_current_org_or_404(request)
    target_member = User.objects.get(pk=user_id)

    if deactivate_org_member(request=request, target_member=target_member, organization=organization):
        return HttpResponseRedirect(reverse_lazy("prescribers_views:members"))

    context = {
        "structure": organization,
        "target_member": target_member,
    }

    return render(request, template_name, context)


@login_required
def update_admin_role(request, action, user_id, template_name="prescribers/update_admins.html"):
    organization = get_current_org_or_404(request)
    target_member = User.objects.get(pk=user_id)

    if update_org_admin_role(request=request, organization=organization, target_member=target_member, action=action):
        return HttpResponseRedirect(reverse_lazy("prescribers_views:members"))

    context = {
        "action": action,
        "structure": organization,
        "target_member": target_member,
    }

    return render(request, template_name, context)


@login_required
def list_accredited_organizations(request, template_name="prescribers/list_accredited_organizations.html"):
    """
    List organizations accredited by a departmental council ("Conseil Départemental").
    """
    prescriber_org = get_current_org_or_404(request)

    required_permissions = [
        prescriber_org.is_authorized,
        prescriber_org.kind == prescriber_org.Kind.DEPT,
        prescriber_org.has_admin(request.user),
    ]

    if not all(required_permissions):
        raise PermissionDenied

    accredited_orgs = PrescriberOrganization.objects.get_accredited_orgs_for(
        prescriber_org
    ).prefetch_active_memberships()

    context = {"prescriber_org": prescriber_org, "accredited_orgs": accredited_orgs}
    return render(request, template_name, context)
