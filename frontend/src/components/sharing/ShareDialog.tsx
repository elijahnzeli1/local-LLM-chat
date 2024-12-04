import React, { useState, useEffect } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  VStack,
  Input,
  Text,
  useToast,
  List,
  ListItem,
  HStack,
  IconButton,
  Badge,
} from '@chakra-ui/react';
import { FiCopy, FiUserPlus, FiUserMinus } from 'react-icons/fi';
import { ShareInvite } from '../../types/sharing';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  conversationId: string;
  currentSharedWith: string[];
  onShare: (email: string) => Promise<void>;
  onRemoveShare: (userId: string) => Promise<void>;
}

export default function ShareDialog({
  isOpen,
  onClose,
  conversationId,
  currentSharedWith,
  onShare,
  onRemoveShare,
}: Props) {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [inviteLink, setInviteLink] = useState('');
  const toast = useToast();

  useEffect(() => {
    if (isOpen) {
      // Generate a shareable link
      setInviteLink(`${window.location.origin}/share/${conversationId}`);
    }
  }, [isOpen, conversationId]);

  const handleShare = async () => {
    if (!email) return;

    try {
      setIsLoading(true);
      await onShare(email);
      setEmail('');
      toast({
        title: 'Shared successfully',
        status: 'success',
        duration: 3000,
      });
    } catch (error) {
      toast({
        title: 'Failed to share',
        description: 'Please try again later',
        status: 'error',
        duration: 3000,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(inviteLink);
    toast({
      title: 'Link copied',
      status: 'success',
      duration: 2000,
    });
  };

  const handleRemoveShare = async (userId: string) => {
    try {
      await onRemoveShare(userId);
      toast({
        title: 'Access removed',
        status: 'success',
        duration: 3000,
      });
    } catch (error) {
      toast({
        title: 'Failed to remove access',
        description: 'Please try again later',
        status: 'error',
        duration: 3000,
      });
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Share Conversation</ModalHeader>
        <ModalBody>
          <VStack spacing={4} align="stretch">
            <Text fontWeight="bold">Share via Email</Text>
            <HStack>
              <Input
                placeholder="Enter email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <IconButton
                aria-label="Share"
                icon={<FiUserPlus />}
                onClick={handleShare}
                isLoading={isLoading}
              />
            </HStack>

            <Text fontWeight="bold" mt={4}>Share via Link</Text>
            <HStack>
              <Input value={inviteLink} isReadOnly />
              <IconButton
                aria-label="Copy link"
                icon={<FiCopy />}
                onClick={handleCopyLink}
              />
            </HStack>

            {currentSharedWith.length > 0 && (
              <>
                <Text fontWeight="bold" mt={4}>Shared With</Text>
                <List spacing={2}>
                  {currentSharedWith.map((userId) => (
                    <ListItem key={userId}>
                      <HStack justify="space-between">
                        <Text>{userId}</Text>
                        <HStack>
                          <Badge colorScheme="green">Active</Badge>
                          <IconButton
                            aria-label="Remove access"
                            icon={<FiUserMinus />}
                            size="sm"
                            colorScheme="red"
                            variant="ghost"
                            onClick={() => handleRemoveShare(userId)}
                          />
                        </HStack>
                      </HStack>
                    </ListItem>
                  ))}
                </List>
              </>
            )}
          </VStack>
        </ModalBody>

        <ModalFooter>
          <Button onClick={onClose}>Close</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
