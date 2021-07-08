from flask import current_app, url_for, abort
from x_app.navigation import XNavigationMixin, XNav


class NavigationViewModel(XNavigationMixin):
    @property
    def navigation(self):
        if not current_app.identity_provider.current_user.is_authenticated:
            return [XNav('Sign In', url_for('auth.login'), 'btn-outline-secondary'),
                    XNav('Sign Up', url_for('auth.register'), 'btn-outline-primary')]
        else:
            return [XNav('Sign Out', url_for('auth.logout'), 'btn-outline-secondary')]
