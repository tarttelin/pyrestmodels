bplist00�      >?T$topX$objectsX$versionY$archiver�  Troot��H 	 
    . / 0 1 2 3 4 < = > ? @ G M P X Y \ b f h p s { � � � � � � � � � � � � � � � � � � � � � � � � � � � � � !)*+,/26:U$null�        _NSAttributeInfo\NSAttributesV$classXNSString�E��G�o� X M L   M o d e l s 
 
 S t a r t i n g   w i t h   a n   e x a m p l e ,   h e r e   w e   m a p   t h e   a d d r e s s   X M L   t o   a n   A d d r e s s   m o d e l : 
 
 < s c r i p t   s r c = " h t t p s : / / g i s t . g i t h u b . c o m / 4 5 5 9 4 4 2 . j s " > < / s c r i p t > 
 
 T h i s   e x a m p l e   w o u l d   b e   u s e d   a s   f o l l o w s : 
 
 > > >   a d d r e s s   =   A d d r e s s ( x m l = e x a m p l e _ a d d r e s s ) 
 > > >   p r i n t (  a d d r e s s   i s   % s ,   % s    %   ( a d d r e s s . n u m b e r ,   a d d r e s s . s t r e e t ) ) 
  2 2 ,   A c a c i a   A v e n u e 
 
 F i e l d   m a p p i n g   c l a s s e s : 
 
 	%� 	 C h a r F i e l d ( x p a t h =  . . .  ,   d e f a u l t =  . . .  ) 
 	%� 	 I n t F i e l d ( x p a t h =  . . .  ,   d e f a u l t =  . . .  ) 
 	%� 	 D a t e F i e l d ( x p a t h =  . . .  ,   d e f a u l t =  . . .  ,   d a t e _ f o r m a t =  % Y - % m - % d T % H : % M : % S  ) 
 	%� 	 F l o a t F i e l d ( x p a t h = " . . . " ,   d e f a u l t = " . . . " ) 
 	%� 	 B o o l F i e l d ( x p a t h = " . . . " ,   d e f a u l t = " . . . " ) 
 	%� 	 C o l l e c t i o n ( f i e l d t y p e ,   o r d e r _ b y = N o n e ,   x p a t h = " . . . " ,   d e f a u l t = " . . . " ) 
 	%� 	 O n e T o O n e F i e l d ( f i e l d t y p e ,   x p a t h =  . . .  ,   d e f a u l t =  . . .  ) 
 
 T h e   f i r s t   5   f i e l d s   a r e   s e l f   e x p l a n a t o r y .     T h e   C o l l e c t i o n   f i e l d   i s   u s e d   t o   m a p   l i s t s   o f   s u b   e l e m e n t s ,   e i t h e r   p r i m i t i v e   t y p e s   o r   o t h e r   x m l _ m o d e l   t y p e s : 
 
 < s c r i p t   s r c = " h t t p s : / / g i s t . g i t h u b . c o m / 4 7 0 9 7 1 6 . j s " > < / s c r i p t > 
 
 T o   m a p   a   c o l l e c t i o n   o f   s t r i n g s ,   t h e   f i e l d t y p e   f o r   t h e   C o l l e c t i o n   f i e l d   w o u l d   b e   C h a r F i e l d . 
 
 N a m e s p a c e s 
 
 N a m e s p a c e   s u p p o r t   i s   v e r y   b a s i c ,   b u t   t h e r e   i s   s u p p o r t   f o r   a   r o o t   l e v e l   n a m e s p a c e ,   w h i c h   c a n   b e   d e f i n e d   o f   t h e   x m l _ m o d e l .     N o t e   t h a t   t h e r e   i s   n o   s u p p o r t   f o r   m u l t i p l e   n a m e s p a c e s   o r   n e s t e d   n a m e s p a c e s . 
 
 < s c r i p t   s r c = " h t t p s : / / g i s t . g i t h u b . c o m / 4 7 1 0 2 5 5 . j s " > < / s c r i p t >�    ZNS.objects�       ����2�5�7�<�D�     ! ' -WNS.keys� " # $ % &�
����� ( ) * + ,�����	�YNSToolTip_$kRWTextViewMarkupDirectivesAttribute_NSBackgroundColorVNSFont_NSParagraphStyleP�     5 8 ;� 6 7��� 9 :���StagTnameRh3_HTMLFormatMenuHeading3� A B C DX$classesZ$classname� D E F_NSMutableDictionary\NSDictionaryXNSObject� H I  J K LUNSRGB\NSColorSpaceO0.8399999738 1 0.8299999833 �� A B N O� O FWNSColor� Q R  S T U V WVNSSizeVNSNameXNSfFlags#@(      ��YHelvetica� A B Z [� [ FVNSFont� ] ^  _ ` aZNSTabStops[NSAlignment� �� A B c e� d F_NSParagraphStyle_NSParagraphStyle� A B g E� E F�     i l -� j %��� , +�	��� ] ^  _ ` a� ��     t w -� u %��� , +�	��� ] ^  | } ~ `  � �[NSTextLists\NSHeadIndent��1�-#@B      �   � �� � � � � � � � � � � � � ��� �!�"�#�$�%�&�'�(�)�*�+�,� �  � �ZNSLocation#@&      �� A B � �� � FYNSTextTabYNSTextTab� �  � � � `_NSTextAlignment#@B      �� �  � �#@L      �� �  � �#@U      �� �  � �#@\      �� �  � �#@a�     �� �  � �#@e      �� �  � �#@h�     �� �  � �#@l      �� �  � �#@o�     �� �  � �#@q�     �� �  � �#@s@     �� �  � �#@u      �� A B � �� � FWNSArray�   � �� Ā.�,� �  � �^NSMarkerFormat�/�0X{circle}� A B � ΢ � FZNSTextListZNSTextList� A B � ӣ � � F_NSMutableParagraphStyle_NSParagraphStyle_NSMutableParagraphStyle�     � � -� u ׀�3� , +�	��� Q R  S � � V �#@(      �4�\LucidaGrande�     � � -� � u ׀6��3� * , +��	��� H I  � � LF1 1 1 ��     � � -� � %�8�� , +�	��� ] ^  | � `  ��9�1�;�   � �� � � � � � � � � � � � ��:�!�"�#�$�%�&�'�(�)�*�+�,� �  �#@<      ��   ���,�     -� % �>�?�C��8� ( * + ,��=���	�_$kRWTextViewMarkupDirectivesAttributeP�    "% ;�#$�A�B� :'��@�Stag_HTMLFormatMenuHeading3Rh3� H I - K LO0.8399999738 1 0.8299999833 �� A B01�1 � F^NSMutableArray�3 45WNS.dataO?
 � ('4'&A6�
��F� A B78�89 F]NSMutableDataVNSData� A B;=�< F_NSAttributedString_NSAttributedString ��_NSKeyedArchiver    ' 0 : ? D F � � �!#%'#,7FHJLNPRTVckvxz|~��������������	!$=FOZaw�������������'05<IT`bdfot�����������������������)+-/8A\^`bdfhjlnprtvx��������������� 	(13<EGPY[dmox���������������������
#.7>Xk�������������������������	!&(*/135FHJLUnprtvxz|~�������������������������	$&(*.GJWvx���������
4IN            @              `