# 🚀 DEPLOYMENT STRATEGY - Script Fury Production

## 🏗️ ENVIRONMENT ARCHITECTURE

### **Three-Tier Deployment Strategy**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   PREVIEW   │───▶│   STAGING   │───▶│ PRODUCTION  │
│  (preview)  │    │  (staging)  │    │   (main)    │
└─────────────┘    └─────────────┘    └─────────────┘
     Fast            Full              Manual
   Testing          Testing           Approval
```

### **Branch-to-Environment Mapping:**
- **`preview`** → Preview Railway Service (auto-deploy)
- **`staging`** → Staging Railway Service (auto-deploy)  
- **`main`** → Production Railway Service (manual deploy)

## 🔒 SECURITY & APPROVAL GATES

### **Preview Environment**
- **Purpose**: Feature development and quick testing
- **Deployment**: Automatic on push to `preview`
- **Quality Gates**: Fast lint + unit tests
- **URL**: `https://script-fury-preview.railway.app`

### **Staging Environment** 
- **Purpose**: Pre-production testing and validation
- **Deployment**: Automatic on merge to `staging`
- **Quality Gates**: Full test suite + integration tests
- **URL**: `https://script-fury-staging.railway.app`

### **Production Environment**
- **Purpose**: Live application for end users
- **Deployment**: MANUAL ONLY with CONFIRM requirement
- **Quality Gates**: Complete security + performance validation
- **URL**: `https://scriptfuryproduction-production.up.railway.app`

## 🚨 PRODUCTION DEPLOYMENT PROTECTION

### **MANDATORY CONFIRMATION PROCESS**

#### **Method 1: Manual Workflow Trigger (RECOMMENDED)**
```bash
# Go to GitHub Actions → Production Deployment
# Click "Run workflow"
# Inputs required:
#   confirmation: "CONFIRM" (exact spelling)
#   reason: "Deploy new features for client demo"
```

#### **Method 2: Pull Request Merge**
```bash
# Create PR: staging → main
# Requires: 2 approvals + all checks pass
# Manual approval in GitHub environment required
# Still requires typing CONFIRM in workflow
```

### **NO BYPASS MECHANISMS**
- ❌ No direct push to main (blocked)
- ❌ No force push (blocked)
- ❌ No admin override (disabled)
- ❌ No emergency bypass (not configured)

## 🔄 STANDARD DEPLOYMENT FLOW

### **Feature Development Process:**
```bash
# 1. Create feature branch
git checkout -b feature/new-storyboard-style
git push -u origin feature/new-storyboard-style

# 2. Development and testing
# Make changes, commit, push

# 3. Deploy to preview for testing
git checkout preview
git merge feature/new-storyboard-style
git push origin preview
# → Auto-deploys to preview environment

# 4. Test preview thoroughly
# → Verify functionality at preview URL

# 5. Promote to staging
git checkout staging  
git merge preview
git push origin staging
# → Auto-deploys to staging environment

# 6. Full staging validation
# → Complete testing of staging environment

# 7. Production deployment (MANUAL)
# Create PR: staging → main
# After approval and merge:
# → Manual workflow trigger required
# → Type CONFIRM + provide reason
```

### **Hotfix Process:**
```bash
# 1. Create hotfix from main
git checkout main
git checkout -b hotfix/critical-bug-fix

# 2. Make minimal fix with tests
# Fix bug, add test, commit

# 3. Fast-track through environments
git checkout preview
git merge hotfix/critical-bug-fix
git push origin preview
# → Test in preview

git checkout staging
git merge preview  
git push origin staging
# → Test in staging

# 4. Emergency production deployment
# Create PR: staging → main (marked as hotfix)
# Manual approval + CONFIRM still required
```

## 🛠️ RAILWAY ENVIRONMENT SETUP

### **Production Service (Existing)**
```yaml
Service: script_fury_production
Environment: production
Domain: scriptfuryproduction-production.up.railway.app
Branch: main
Auto-deploy: false (manual only)
```

### **Staging Service (To Create)**
```yaml
Service: script_fury_staging  
Environment: staging
Domain: script-fury-staging.railway.app
Branch: staging
Auto-deploy: true
```

### **Preview Service (To Create)**
```yaml
Service: script_fury_preview
Environment: preview  
Domain: script-fury-preview.railway.app
Branch: preview
Auto-deploy: true
```

### **Environment Variables (All Environments)**
```bash
# Core Configuration
OPENAI_API_KEY=<secret>
MODEL_MODE=balanced
CHARACTER_MODEL=gpt-4o
SCENE_MODEL=gpt-4o
SANITIZATION_MODEL=o3-mini
INFO_MODEL=gpt-4o-mini
IMAGE_MODEL=gpt-image-1

# Environment-specific
FLASK_ENV=production|staging|development
FLASK_DEBUG=false|true|true
```

## 📊 MONITORING & ALERTS

### **Deployment Monitoring**
- **Production**: Full uptime monitoring + alerts
- **Staging**: Basic monitoring for testing
- **Preview**: Minimal monitoring

### **Success Metrics**
- **Deployment Time**: < 5 minutes
- **Test Success Rate**: 100% required for production
- **Rollback Time**: < 2 minutes if needed

### **Alert Channels**
- **Production Failures**: Immediate notification
- **Staging Issues**: Daily summary
- **Preview Problems**: No alerts (development only)

## 🔍 QUALITY GATES BY ENVIRONMENT

### **Preview Quality Gates**
- ✅ Syntax validation
- ✅ Basic lint checks  
- ✅ Unit tests only
- ✅ App startup test

### **Staging Quality Gates**
- ✅ Full lint with strict rules
- ✅ Complete test suite
- ✅ Integration tests
- ✅ Code formatting validation
- ✅ Security baseline scan

### **Production Quality Gates**
- ✅ Everything from staging PLUS:
- ✅ Full security audit
- ✅ Performance benchmarks
- ✅ Coverage requirements (>90%)
- ✅ Manual code review (2 approvers)
- ✅ Final integration test
- ✅ Manual confirmation (CONFIRM)

## 🎯 ROLLBACK STRATEGY

### **Automatic Rollback Triggers**
- Health check failures > 3 minutes
- Error rate > 5% for 2 minutes
- Memory usage > 90% for 5 minutes

### **Manual Rollback Process**
```bash
# 1. Identify last known good deployment
git log --oneline main -10

# 2. Create rollback branch
git checkout -b rollback/to-commit-abc123
git reset --hard abc123

# 3. Emergency deployment
# Use same CONFIRM process for rollback
# Reason: "Emergency rollback to abc123"
```

## 📋 DEPLOYMENT CHECKLIST

### **Before Any Production Deployment:**
- [ ] All tests passing in staging environment
- [ ] Manual testing completed in staging
- [ ] Performance acceptable in staging
- [ ] Security scan results reviewed
- [ ] Rollback plan identified
- [ ] Team notification sent
- [ ] CONFIRM typed correctly
- [ ] Deployment reason documented

### **After Production Deployment:**
- [ ] Health check passing
- [ ] Core functionality verified
- [ ] Performance metrics normal
- [ ] Error logs reviewed
- [ ] Team notified of success
- [ ] Documentation updated if needed

## 🚀 SETUP COMMANDS

### **Initial Railway Services Setup**
```bash
# Create staging service
railway new --name script-fury-staging
railway connect script-fury-staging
railway env set FLASK_ENV=staging

# Create preview service  
railway new --name script-fury-preview
railway connect script-fury-preview
railway env set FLASK_ENV=development
```

**Remember: Security first, quality second, speed third. No shortcuts to production.** 🔒