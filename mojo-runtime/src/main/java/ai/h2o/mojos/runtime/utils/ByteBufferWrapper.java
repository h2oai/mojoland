package ai.h2o.mojos.runtime.utils;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;


/**
 * Simplified version and drop-in replacement of water.util.AutoBuffer
 */
public final strictfp class ByteBufferWrapper {
  private ByteBuffer bb;

  /** Wrap a fixed byte[] array. */
  public ByteBufferWrapper(byte[] buf, ByteOrder endianness) {
    assert buf != null : "null fed to ByteBuffer.wrap";
    bb = ByteBuffer.wrap(buf, 0, buf.length).order(endianness);
  }

  /** Current buffer position. */
  public int position() {
    return bb.position();
  }

  /** Skip over some bytes in the byte buffer. Caller is responsible for not reading off end of the bytebuffer. */
  public void skip(int skip) {
    bb.position(bb.position() + skip);
  }

  // -----------------------------------------------
  // Unlike original getX() methods, these will not attempt to auto-widen the buffer.

  public int get1U() {
    return bb.get() & 0xFF;
  }
  public char get2() {
    return bb.getChar();
  }
  public int get3() {
    return get1U() | (get1U() << 8) | (get1U() << 16);
  }
  public int get4() {
    return bb.getInt();
  }
  public float get4f() {
    return bb.getFloat();
  }
}
