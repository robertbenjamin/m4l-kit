import CoreGraphics
import Foundation
let opts = CGWindowListOption(arrayLiteral: .optionOnScreenOnly, .excludeDesktopElements)
let list = CGWindowListCopyWindowInfo(opts, kCGNullWindowID) as! [[String: Any]]
for w in list {
  let owner = w[kCGWindowOwnerName as String] as? String ?? ""
  let name = w[kCGWindowName as String] as? String ?? ""
  let id = w[kCGWindowNumber as String] as? Int ?? 0
  let layer = w[kCGWindowLayer as String] as? Int ?? 0
  let b = w[kCGWindowBounds as String] as? [String: Any] ?? [:]
  if layer == 0 { print("\(id)\t\(owner)\t\(name)\t\(b["X"]!),\(b["Y"]!),\(b["Width"]!),\(b["Height"]!)") }
}
