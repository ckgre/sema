import os
import json
import logging
import argparse
import sys
sys.path.append('../../utils')
from utils.utils import create_new_dir, count_errors
from utils.mylogger import *

def innerVisitor(A: list, inners):
  for item in A:
    tmp = {}
    visit(item, tmp)
    if tmp != {}:
      inners.append(tmp)

def visitAttr(A: dict, Out: dict):
  id = A["id"]
  Out["kind"] = A["Kind"]
  tmp = {}
  writeSourceRange(A["range"], tmp)
  if tmp != {}:
    Out["range"] = tmp
  if "inherited" in A:
    pass
  if "implicit" in A:
    pass
  
  if "inner" in A:
    inners = []
    innerVisitor(A["inners"], inners)
    if len(inners) >= 1:
      Out["inner"] = inners

def visitStmt(S: dict, Out):
  id = S["id"]
  Out["kind"] = S["kind"]
  tmp = {}
  writeSourceRange(S["range"], tmp)
  if tmp != {}:
    Out["range"] = tmp
  if "type" in S:
    pass
  if "valueCategory" in S:
    pass
  
  if "inner" in S:
    inners = []
    innerVisitor(S["inner"], inners)
    if len(inners) >= 1:
      Out["inner"] = inners

  if S["kind"] == "IfStmt":
    visitIfStmt(S, Out)
  elif S["kind"] == "SwitchStmt":
    visitSwitchStmt(S, Out)
  elif S["kind"] == "CaseStmt":
    visitCaseStmt(S, Out)
  elif S["kind"] == "LabelStmt":
    visitLabelStmt(S, Out)
  elif S["kind"] == "GotoStmt":
    visitGotoStmt(S, Out)
  elif S["kind"] == "whileStmt":
    visitWhileStmt(S, Out)
  else:
    pass

def visitType(T: dict, Out):
  id = T["id"]
  Out["kind"] = T["kind"]
  tmp = {}
  createQualType(T["type"], tmp)
  if tmp != {}:
    Out["type"] = tmp
  if "containsErrors" in T:
    pass
  if "isDependent" in T:
    pass
  if "isInstantiationDependent" in T:
    pass
  if "isVariablyModified" in T:
    pass
  if "containsUnexpandedPack" in T:
    pass
  if "isImported" in T:
    pass
  
  if "inner" in T:
    inners = []
    innerVisitor(T["inner"], inners)
    if len(inners) >= 1:
      Out["inner"] = inners
  if T["kind"] == "TypedefType":
    visitTypedefType(T, Out)
  elif T["kind"] == "FunctionType": 
    visitFunctionType(T, Out)
  elif T["kind"] == "FunctionProtoType":
    visitFunctionProtoType(T, Out)
  elif T["kind"] == "RValueReferenceType":
    visitRValueReferenceType(T, Out)
  elif T["kind"] == "ArrayType":
    visitArrayType(T, Out)
  elif T["kind"] == "ConstantArrayType":
    visitConstantArrayType(T, Out)
  elif T["kind"] == "DependentSizedExtVectorType":
    visitDependentSizedExtVectorType(T, Out)
  elif T["kind"] == "UnresolvedUsingType":
    visitUnresolvedUsingType(T, Out)
  elif T["kind"] == "UnaryTransformType":
    visitUnaryTransformType(T, Out)
  elif T["kind"] == "TagType":
    visitTagType(T, Out)
  elif T["kind"] == "AutoType":
    visitAutoType(T, Out)
  elif T["kind"] == "ElaboratedType":
    visitElaboratedType(T, Out)
  elif T["kind"] == "MacroQualifiedType":
    visitMacroQualifiedType(T, Out)
  elif T["kind"] == "MemberPointerType":
    visitMemberPointerType(T, Out)
  else:
    pass

def visitQualType(T: dict, Out):
  id = T["id"]
  kind = T["kind"]
  Out["type"] = createQualType(T["type"], Out)
  qualifiers = T["qualifiers"]

def visitDecl(D: dict, Out):
  id = D["id"]
  Out["kind"] = D["kind"]
  loctmp = {}
  writeSourceLocation(D["loc"], loctmp)
  if loctmp != {}:
    Out["loc"] = loctmp
  rangetmp = {}
  writeSourceRange(D["range"], rangetmp)
  if rangetmp != {}:
    Out["range"] = rangetmp
  if "isImplicit" in D:
    pass
  if "isInvalid" in D:
    pass
  if "isUsed" in D:
    pass
  if "isReferenced" in D:
    pass
  if "isHidden" in D:
    pass
  if "parentDeclContextId" in D:
    pass
  if "inner" in D:
    inners = []
    innerVisitor(D["inner"], inners)
    if len(inners) >= 1:
      Out["inner"] = inners
  if D["kind"] == "NamedDecl":
    visitNamedDecl(D, Out)
  elif D["kind"] == "TypedefDecl":
    visitTypedefDecl(D, Out)
  elif D["kind"] == "TypeAliasDecl":
    visitTypeAliasDecl(D, Out)
  elif D["kind"] == "UsingDecl":
    visitUsingDecl(D, Out)
  elif D["kind"] == "UsingEnumDecl":
    visitUsingEnumDecl(D, Out)
  elif D["kind"] == "UsingShadowDecl":
    visitUsingShadowDecl(D, Out)
  elif D["kind"] == "VarDecl":
    visitVarDecl(D, Out)
  elif D["kind"] == "FieldDecl":
    visitFieldDecl(D, Out)
  elif D["kind"] == "FunctionDecl":
    visitFunctionDecl(D, Out)
  elif D["kind"] == "EnumDecl":
    visitEnumDecl(D, Out)
  elif D["kind"] == "EnumConstantDecl":
    visitEnumConstantDecl(D, Out)
  elif D["kind"] == "RecordDecl":
    visitRecordDecl(D, Out)
  elif D["kind"] == "BlockDecl":
    visitBlockDecl(D, Out)
  else:
    pass

def visitExpr(E: dict, Out):
  if E["kind"] == "DeclRefExpr":
    visitDeclRefExpr(E, Out)
  elif E["kind"] == "SYCLUniqueStableNameExpr":
    visitSYCLUniqueStableNameExpr(E, Out)
  elif E["kind"] == "PredefinedExpr":
    visitPredefinedExpr(E, Out)
  elif E["kind"] == "MemberExpr":
    visitMemberExpr(E, Out)
  elif E["kind"] == "CastExpr":
    visitCastExpr(E, Out)
  elif E["kind"] == "ImplicitCastExpr":
    visitImplicitCastExpr(E, Out)
  elif E["kind"] == "CallExpr":
    visitCallExpr(E, Out)
  elif E["kind"] == "UnaryExpr" or E["kind"] == "TypeTraitExpr":
    visitUnaryExprOrTypeTraitExpr(E, Out)
  elif E["kind"] == "SizeOfPackExpr":
    visitSizeOfPackExpr(E, Out)
  elif E["kind"] == "UnresolvedLookupExpr":
    visitUnresolvedLookupExpr(E, Out)
  elif E["kind"] == "AddrLabelExpr":
    visitAddrLabelExpr(E, Out)
  elif E["kind"] == "ConstantExpr":
    visitConstantExpr(E, Out)
  elif E["kind"] == "InitListExpr":
    visitInitListExpr(E, Out)
  elif E["kind"] == "RequiresExpr":
    visitRequiresExpr(E, Out)
  else:
    pass
  if "inner" in E:
    inners = []
    innerVisitor(E["inner"], inners)
    if len(inners) >= 1:
      Out["inner"] = inners

def visitOperator(O: dict, Out):
  if O["kind"] == "UnaryOperator":
    visitUnaryOperator(O, Out)
  elif O["kind"] == "BinaryOperator":
    visitBinaryOperator(O, Out)
  elif O["kind"] == "CompoundAssignOperator":
    visitCompoundAssignOperator(O, Out)
  else:
    pass
  if "inner" in O:
    inners = []
    innerVisitor(O["inner"], inners)
    if len(inners) >= 1:
      Out["inner"] = inners

def visitLiteral(L, Out):
  if L["kind"] == "IntegerLiteral":
    visitIntegerLiteral(L, Out)
  elif L["kind"] == "CharacterLiteral":
    visitCharacterLiteral(L, Out)
  elif L["kind"] == "FixedPointLiteral":
    visitFixedPointLiteral(L, Out)
  elif L["kind"] == "FloatingLiteral":
    visitFloatingLiteral(L, Out)
  elif L["kind"] == "StringLiteral":
    visitStringLiteral(L, Out)
  else:
    pass
  if "inner" in L:
    inners = []
    innerVisitor(L["inner"], inners)
    if len(inners) >= 1:
      Out["inner"] = inners

def visitAPValue(Value: dict, Out):
  Out["value"] = Value["value"]

def writeIncludeStack(Loc: dict, Out):
  if "includedFrom" in Loc:
    pass

def writeBareSourceLocation(Loc: dict, Out):
  if "offset" in Loc:
    pass
  if "file" in Loc:
    pass
  if "line" in Loc:
    Out["line"] = Loc["line"]
  if "presumedFile" in Loc:
    pass
  col = Loc["col"]
  toklen = Loc["tokLen"]

  writeIncludeStack(Loc, Out)

def writeSourceLocation(Loc: dict, Out):
  if "spellingLoc" in Loc and "expansionLoc" in Loc:
    spelltmp = {}
    writeBareSourceLocation(Loc["spellingLoc"], spelltmp)
    if spelltmp != {}:
      Out["spellingLoc"] = spelltmp
    exptmp = []
    writeBareSourceLocation(Loc["expansionLoc"], exptmp)
    if exptmp != {}:
      if "isMacroArgExpansion" in Loc["expansionLoc"]:
        pass
      Out["expansionLoc"] = exptmp
  else:
    writeBareSourceLocation(Loc, Out)

def writeSourceRange(R: dict, Out: dict):
  begin = {}
  writeSourceLocation(R["begin"], begin)
  if begin != {}:
    Out["begin"] = begin
  end = {}
  writeSourceLocation(R["end"], end)
  if end != {}:
    Out["end"] = end

def createQualType(QT: dict, Out):
  if "qualType" in QT:
    pass
  if "desugaredQualType" in QT:
    pass
  if "typeAliasDeclId" in QT:
    pass

def writeBareDeclRef(D: dict, Out):
  id = D["id"]
  Out["kind"] = D["kind"]
  if "name" in D:
    Out["name"] = D["name"]
  if "type" in D:
    pass

def createBareDeclRef(D: dict, Out):
  id = D["id"]
  Out["kind"] = D["kind"]
  if "name" in D:
    Out["name"] = D["name"]
  if "type" in D:
    pass

def visitTypedefType(TT: dict, Out):
  Out["decl"] = TT["decl"]

def visitFunctionType(T: dict, Out):
  if "noreturn" in T:
    pass
  if "producesResult" in T:
    pass
  if "regParm" in T:
    pass
  cc = T["cc"]

def visitFunctionProtoType(T: dict, Out):
  if "trailingReturn" in T:
    pass
  if "const" in T:
    pass
  if "volatile" in T:
    pass
  if "restrict" in T:
    pass
  if "variadic" in T:
    pass
  if "refQualifier" in T:
    pass
  if "exceptionSpec" in T:
    pass
  if "throwsAny" in T:
    pass
  if "conditionEvaluatesTo" in T:
    pass
  visitFunctionType(T, Out)

def visitRValueReferenceType(RT: dict, Out):
  if "spelledAsLValue" in RT:
    pass

def visitArrayType(AT: dict, Out):
  if "sizeModifier" in AT:
    pass
  if "indexTypeQualifiers" in AT:
    pass

def visitConstantArrayType(CAT: dict, Out):
  size = CAT["size"]
  visitArrayType(CAT, Out)

def visitDependentSizedExtVectorType(VT: dict, Out):
  if "attrLoc" in VT:
    tmp = {}
    writeSourceLocation(VT["attrLoc"], tmp)
    if tmp != {}:
      Out["attrLoc"] = tmp

def visitUnresolvedUsingType(UUT: dict, Out):
  tmp = {}
  createBareDeclRef(UUT["decl"], tmp)
  if tmp != {}:
    Out["decl"] = tmp

def visitUnaryTransformType(UTT: dict, Out):
  if "transformKind" in UTT:
    pass

def visitTagType(TT: dict, Out):
  tmp = {}
  createBareDeclRef(TT["decl"], tmp)
  if tmp != {}:
    Out["decl"] = tmp

def visitAutoType(AT: dict, Out):
  undeduced = AT["undeduced"]
  if "typeKeyword" in AT:
    pass

def visitElaboratedType(ET: dict, Out):
  if "qualifier" in ET:
    pass
  if "ownedTagDecl" in ET:
    tmp = {}
    createBareDeclRef(ET["ownedTagDecl"], tmp)
    if tmp != {}:
      Out["ownedTagDecl"] = tmp

def visitMacroQualifiedType(MQT: dict, Out):
  marcoName = MQT["macroName"]

def visitMemberPointerType(MPT: dict, Out):
  if "isData" in MPT:
    pass
  if "isFunction" in MPT:
    pass

def visitNamedDecl(ND: dict, Out):
  if "name" in ND:
    Out["name"] =  ND["name"]
  if "mangledName" in ND:
    Out["mangledName"] = ND["mangledName"]

def visitTypedefDecl(TD: dict, Out):
  visitNamedDecl(TD, Out)
  tmp = {}
  createQualType(TD["type"], tmp)
  if tmp != {}:
    Out["type"] = tmp

def visitTypeAliasDecl(TAD: dict, Out):
  visitTypeAliasDecl(TAD, Out)
  tmp = {}
  createQualType(TAD["type"], tmp)
  if tmp != {}:
    Out["type"] = tmp

def visitUsingDecl(UD, Out):
  Out["name"] = UD["name"]

def visitUsingEnumDecl(UED, Out):
  tmp = {}
  createBareDeclRef(UED["target"], tmp)
  if tmp != {}:
    Out["target"] = tmp

def visitUsingShadowDecl(USD, Out):
  tmp = {}
  createBareDeclRef(USD["target"], tmp)
  if tmp != {}:
    Out["target"] = tmp

def visitVarDecl(VD, Out):
  visitNamedDecl(VD, Out)
  Out["type"] = VD["type"]
  if "storageClass" in VD:
    pass
  if "tls" in VD:
    pass
  if "nrvo" in VD:
    pass
  if "inline" in VD:
    pass
  if "constexpr" in VD:
    pass
  if "modulePrivate" in VD:
    pass
  if "init" in VD:
    pass
  if "isParameterPack" in VD:
    pass

def visitFieldDecl(FD, Out):
  visitNamedDecl(FD, Out)
  tmp = {}
  createQualType(FD["type"], tmp)
  if tmp != {}:
    Out["type"] = tmp
  if "mutable" in FD:
    pass
  if "modulePrivate" in FD:
    pass
  if "isBitfield" in FD:
    pass
  if "hasInClassInitializer" in FD:
    pass

def visitFunctionDecl(FD, Out):
  visitNamedDecl(FD, Out)
  tmp = {}
  createQualType(FD["type"], tmp)
  if tmp != {}:
    Out["type"] = tmp
  if "storageClass" in FD:
    pass
  if "inline" in FD:
    pass
  if "virtual" in FD:
    pass
  if "pure" in FD:
    pass
  if "explicitlyDeleted" in FD:
    pass
  if "constexpr" in FD:
    pass
  if "variadic" in FD:
    pass
  if "explicitlyDefaulted" in FD:
    pass

def visitEnumDecl(ED, Out):
  visitNamedDecl(ED, Out)
  if "fixedUnderlyingType" in ED:
    pass
  if "scopedEnumTag" in ED:
    pass

def visitEnumConstantDecl(ECD, Out):
  visitNamedDecl(ECD, Out)
  tmp = {}
  createQualType(ECD["type"], tmp)
  if tmp != {}:
    Out["type"] = tmp

def visitRecordDecl(RD, Out):
  visitNamedDecl(RD, Out)
  Out["tagUsed"] = RD["tagUsed"]
  if "completeDefinition" in RD:
    pass

def visitBlockDecl(D, Out):
  if "variadic" in D:
    pass
  if "capturesThis" in D:
    pass

def visitDeclRefExpr(DRE, Out):
  decltmp = {}
  createBareDeclRef(DRE["referencedDecl"], decltmp)
  if decltmp != {}:
    Out["referencedDecl"] = decltmp
  if "foundReferencedDecl" in DRE:
    tmp = {}
    createBareDeclRef(DRE["foundReferencedDecl"], tmp)
    if tmp != {}:
      Out["foundReferencedDecl"] = tmp
  if "nonOdrUseReason" in DRE:
    pass

def visitSYCLUniqueStableNameExpr(E, Out):
  tmp = {}
  createQualType(E, tmp)
  if tmp != {}:
    Out["typeSourceInfo"] = tmp

def visitPredefinedExpr(PE, Out):
  Out["name"] = PE["name"]

def visitUnaryOperator(UO, Out):
  Out["isPostfix"] = UO["isPostfix"]
  Out["opcode"] = UO["opcode"]
  if "canOverflow" in UO:
    pass

def visitBinaryOperator(BO, Out):
  Out["opcode"] = BO["opcode"]

def visitCompoundAssignOperator(CAO, Out):
  visitBinaryOperator(CAO, Out)
  lhstmp = {}
  createQualType(CAO["computeLHSType"], lhstmp)
  if lhstmp != {}:
    pass
  restmp = {}
  createQualType(CAO["computeResultType"], restmp)
  if restmp != {}:
    pass

def visitMemberExpr(ME, Out):
  Out["name"] = ME["name"]
  Out["isArrow"] = ME["isArrow"]
  Out["referencedMemberDecl"] = ME["referencedMemberDecl"]
  if "nonOdrUseReason" in ME:
    pass

def visitCastExpr(CE, Out):
  Out["castKind"] = CE["castKind"]
  if "path" in CE:
    Out["path"] = CE["path"]
  if "conversionFunc" in CE:
    pass

def visitImplicitCastExpr(ICE, Out):
  visitCastExpr(ICE, Out)
  if "isPartOfExplicitCast" in ICE:
    pass

def visitCallExpr(CE, Out):
  if "adl" in CE:
    pass

def visitUnaryExprOrTypeTraitExpr(TTE, Out):
  Out["name"] = TTE["name"]
  if "argType" in TTE:
    pass

def visitSizeOfPackExpr(SOPE, Out):
  visitNamedDecl(SOPE)

def visitUnresolvedLookupExpr(ULE, Out):
  Out["usesADL"] = ULE["usesADL"]
  Out["name"] = ULE["name"]
  Out["lookups"] = ULE["lookups"]

def visitAddrLabelExpr(ALE, Out):
  Out["name"] = ALE["name"]
  Out["labelDeclId"] = ALE["labelDeclId"]

def visitConstantExpr(CE, Out):
  visitAPValue(CE, Out)

def visitInitListExpr(ILE, Out):
  if "field" in ILE:
    Out["field"] = ILE["field"]

def visitExprWithCleanups(EWC, Out):
  if "cleanupsHaveSideEffects" in EWC:
    pass
  if "cleanups" in EWC:
    cleanups = []
    for item in EWC["cleanups"]:
      tmp = {}
      if "id" in item:
        pass
      if "kind" in item:
        tmp["kind"] = item["kind"]
      if tmp != {}:
        cleanups.append(tmp)
    if len(cleanups) >= 1:
      Out["cleanups"] = cleanups

def visitRequiresExpr(RE, Out):
  if "satisfied" in RE:
    pass

def visitIntegerLiteral(IL, Out):
  Out["value"] = IL["value"]

def visitCharacterLiteral(CL, Out):
  Out["value"] = CL["value"]

def visitFixedPointLiteral(FPL, Out):
  Out["value"] = FPL["value"]

def visitFloatingLiteral(FL, Out):
  Out["value"] = FL["value"]

def visitStringLiteral(SL, Out):
  Out["value"] = SL["value"]

def visitIfStmt(IS, Out):
  if "hasInit" in IS:
    Out["hasInit"] = IS["hasInit"]
  if "hasVar" in IS:
    Out["hasVar"] = IS["hasVar"]
  if "hasElse" in IS:
    Out["hasElse"] = IS["hasElse"]
  if "isConstexpr" in IS:
    pass
  if "isConsteval" in IS:
    pass
  if "constevalIsNegated" in IS:
    pass

def visitSwitchStmt(SS, Out):
  if "hasInit" in SS:
    Out["hasInit"] = SS["hasInit"]
  if "hasVar" in SS:
    Out["hasVar"] = SS["hasVar"]

def visitCaseStmt(CS, Out):
  if "isGNURange" in CS:
    pass

def visitLabelStmt(LS, Out):
  Out["name"] = LS["name"]
  Out["declId"] = LS["declId"]
  if "sideEntry" in LS:
    pass

def visitGotoStmt(GS, Out):
  Out["targetLabelDeclId"] = GS["targetLabelDeclId"]

def visitWhileStmt(WS, Out):
  if "hasVar" in WS:
    Out["hasVar"] = WS["hasVar"]

Attr = 0
Stmt = 1
Type = 2
QualType = 3
Decl = 4
APValue = 5
Expr = 6
Operator = 7
Literal = 8
UNK = 9

def getKind(item: dict):
  if "kind" in item:
    if item["kind"].endswith("Attr"):
      return Attr
    if item["kind"].endswith("Stmt"):
      return Stmt
    if item["kind"].endswith("Type"):
      return Type
    if item["kind"].endswith("QualType"):
      return QualType
    if item["kind"].endswith("Decl"):
      return Decl
    if "value" in item:
      return APValue
    if item["kind"].endswith("Expr"):
      return Expr
    if item["kind"].endswith("Operator"):
      return Operator
    if item["kind"].endswith("Literal"):
      return Literal
  return UNK

def visit(ast, Out):
  if ast == {}:
    return -1
  kind = getKind(ast)
  if kind == Attr:
    visitAttr(ast, Out)
  elif kind == Stmt:
    visitStmt(ast, Out)
  elif kind == Type:
    visitType(ast, Out)
  elif kind == QualType:
    visitQualType(ast, Out)
  elif kind == Decl:
    visitDecl(ast, Out)
  elif kind == APValue:
    visitAPValue(ast, Out)
  elif kind == Expr:
    visitExpr(ast, Out)
  elif kind == Operator:
    visitOperator(ast, Out)
  elif kind == Literal:
    visitLiteral(ast, Out)
  else:
    raise TypeError
  return 0

def visit_file(_params):
  infile = _params[0]
  outpath = _params[1]
  with open(infile, 'r') as f:
    logger.warning(wcolor.format(f"loading {infile}"))
    ast = json.load(f)
    Out = {}
    logger.warning(wcolor.format(f"visiting ast"))
    ret = visit(ast["main"][0], Out)
    if ret == 0:
      outfile = os.path.join(outpath, os.path.basename(infile))
      logger.warning(scolor.format(f"dump json to {outfile}"))
      of = open(outfile, 'w')
      json.dump(Out, of)
      of.close()
    else:
      errorer.error(ecolor.format(f"ERROR when visit {infile}"))

def batch_visit(path, process, error_log):
  path = os.path.abspath(path)
  _files = [os.path.join(path, _f) for _f in os.listdir(path)]
  logger.warning(wcolor.format(f"Begin to process ast files in {path}"))
  _out_dir = os.path.join(os.path.dirname(path), 'simple-ast')
  logger.warning(wcolor.format(f"Json files of ASTs will be save to {_out_dir}"))
  _out_dir = create_new_dir(_out_dir)
  logger.warning(wcolor.format(f"Creating output directory {_out_dir}"))
  os.makedirs(_out_dir)
  logger.warning(scolor.format("Begin visiting ASTs..."))
  _params = [(_f, _out_dir) for _f in _files]

  from multiprocessing import Pool
  with Pool(process) as p:
    p.map(visit_file, _params)

  err_cnt = count_errors(_files, os.listdir(_out_dir), error_log, ".json")
  logger.warning(scolor.format(f"{len(_files)-err_cnt} of {len(_files)} are successfully dumped to .json files."))
  if err_cnt > 0:
    errorer.error(ecolor.format(f"{err_cnt} encounted errors when visit. Please read {error_log} to check them."))
  
  return len(_files) - err_cnt

def main():
  parser = argparse.ArgumentParser(add_help=True)
  parser.add_argument('-i', "--input", help="Path of full-ast jsonfiles. dir", required=True)
  parser.add_argument('-p', "--process-num", help="Number of process to create.", required=False, default=8, type=int)
  parser.add_argument('-e', "--error-log", help="Output failed compiled files' list to this file.", required=False, default='error.log')
  parser.add_argument('-v', '--version', action='version', help="Show program's version number and exit", version="%(prog)s 1.0")

  args = parser.parse_args()

  if not os.path.isdir(args.input):
    print("\033[31mINPUT option ERROR. Please input a directory.\n\033[0m")
    parser.print_help()
  else:
    logger.warning(scolor.format(f"Use {args.process_num} processes"))
    cnt = batch_visit(args.input, args.process_num, args.error_log)
  return cnt

if __name__ == "__main__":
  main()