package com.liora.oncology.db;

import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;
import android.util.Base64;

import java.nio.charset.StandardCharsets;
import java.security.KeyStore;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;

/**
 * Encrypts and decrypts text before it is stored in a database TEXT column.
 *
 * Requires API 23. The AES-256 key stays in the Android Keystore on this
 * phone. A database copied to another device cannot be decrypted there.
 *
 * Stored value is Base64 of a 12-byte IV followed by the AES-GCM ciphertext
 * and tag. Save that string as-is. Do not trim it.
 *
 * <pre>
 * DbTextCipher cipher = new DbTextCipher();
 * String stored = cipher.encrypt(treatmentText);
 * // INSERT INTO guides(treatment_1) VALUES (?)
 * String plain = cipher.decrypt(stored);
 * </pre>
 */
public final class DbTextCipher {
    private static final String ANDROID_KEYSTORE = "AndroidKeyStore";
    private static final String KEY_ALIAS = "liora.oncology.db.text";
    private static final String TRANSFORMATION = "AES/GCM/NoPadding";
    private static final int GCM_IV_BYTES = 12;
    private static final int GCM_TAG_BITS = 128;

    private final SecretKey key;

    public DbTextCipher() {
        try {
            this.key = loadOrCreateKey();
        } catch (Exception ex) {
            throw new IllegalStateException("Could not open the database text key", ex);
        }
    }

    /** Returns a Base64 string safe to store in a TEXT column. */
    public String encrypt(String plain) {
        if (plain == null) {
            throw new IllegalArgumentException("plain text is required");
        }
        try {
            Cipher cipher = Cipher.getInstance(TRANSFORMATION);
            cipher.init(Cipher.ENCRYPT_MODE, key);
            byte[] iv = cipher.getIV();
            if (iv == null || iv.length != GCM_IV_BYTES) {
                throw new IllegalStateException("AES-GCM IV was not 12 bytes");
            }
            byte[] body = cipher.doFinal(plain.getBytes(StandardCharsets.UTF_8));
            byte[] packed = new byte[iv.length + body.length];
            System.arraycopy(iv, 0, packed, 0, iv.length);
            System.arraycopy(body, 0, packed, iv.length, body.length);
            return Base64.encodeToString(packed, Base64.NO_WRAP);
        } catch (IllegalStateException ex) {
            throw ex;
        } catch (Exception ex) {
            throw new IllegalStateException("Could not encrypt database text", ex);
        }
    }

    /** Reverses a value produced by {@link #encrypt(String)}. */
    public String decrypt(String stored) {
        if (stored == null || stored.isEmpty()) {
            throw new IllegalArgumentException("stored text is required");
        }
        try {
            byte[] packed = Base64.decode(stored, Base64.NO_WRAP);
            if (packed.length <= GCM_IV_BYTES) {
                throw new IllegalArgumentException("stored text is too short");
            }
            byte[] iv = new byte[GCM_IV_BYTES];
            byte[] body = new byte[packed.length - GCM_IV_BYTES];
            System.arraycopy(packed, 0, iv, 0, GCM_IV_BYTES);
            System.arraycopy(packed, GCM_IV_BYTES, body, 0, body.length);
            Cipher cipher = Cipher.getInstance(TRANSFORMATION);
            cipher.init(Cipher.DECRYPT_MODE, key, new GCMParameterSpec(GCM_TAG_BITS, iv));
            byte[] plain = cipher.doFinal(body);
            return new String(plain, StandardCharsets.UTF_8);
        } catch (IllegalArgumentException ex) {
            throw ex;
        } catch (Exception ex) {
            throw new IllegalStateException("Could not decrypt database text", ex);
        }
    }

    private static SecretKey loadOrCreateKey() throws Exception {
        KeyStore keyStore = KeyStore.getInstance(ANDROID_KEYSTORE);
        keyStore.load(null);
        if (!keyStore.containsAlias(KEY_ALIAS)) {
            KeyGenerator generator = KeyGenerator.getInstance(
                    KeyProperties.KEY_ALGORITHM_AES,
                    ANDROID_KEYSTORE);
            generator.init(new KeyGenParameterSpec.Builder(
                    KEY_ALIAS,
                    KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)
                    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                    .setKeySize(256)
                    .setRandomizedEncryptionRequired(true)
                    .build());
            generator.generateKey();
        }
        return (SecretKey) keyStore.getKey(KEY_ALIAS, null);
    }
}
