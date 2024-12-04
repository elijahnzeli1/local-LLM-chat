export interface ShareInvite {
  id: string;
  conversationId: string;
  invitedBy: string;
  invitedEmail: string;
  status: 'pending' | 'accepted' | 'rejected' | 'expired';
  createdAt: string;
  expiresAt: string;
}

export interface ShareSettings {
  enabled: boolean;
  maxShares: number;
  inviteExpirationHours: number;
  allowLinkSharing: boolean;
  allowEmailSharing: boolean;
  requireApproval: boolean;
}

export interface SharePermissions {
  canView: boolean;
  canEdit: boolean;
  canShare: boolean;
  canDelete: boolean;
}

export interface ShareResponse {
  success: boolean;
  inviteId?: string;
  error?: string;
}
